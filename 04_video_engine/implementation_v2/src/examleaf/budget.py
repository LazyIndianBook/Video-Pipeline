"""Atomic local budget reservation: cents, idempotency, and no silent overspend."""
from pathlib import Path
import sqlite3

class BudgetLedger:
    def __init__(self,path:Path,limit_cents:int):
        if limit_cents<0:raise ValueError('negative budget')
        self.path=path;self.limit=limit_cents
        with sqlite3.connect(path) as db:
            db.execute('CREATE TABLE IF NOT EXISTS jobs (key TEXT PRIMARY KEY, cents INTEGER NOT NULL, state TEXT NOT NULL)')
    def reserve(self,key:str,cents:int)->bool:
        if cents<0 or not key:raise ValueError('invalid reservation')
        with sqlite3.connect(self.path,timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            existing=db.execute('SELECT cents,state FROM jobs WHERE key=?',(key,)).fetchone()
            if existing:
                if existing[0]!=cents:raise ValueError('idempotency key reused with different cost')
                return False
            total=db.execute("SELECT COALESCE(SUM(cents),0) FROM jobs WHERE state!='released'").fetchone()[0]
            if total+cents>self.limit:raise RuntimeError('budget would be exceeded')
            db.execute('INSERT INTO jobs VALUES (?,?,?)',(key,cents,'reserved'))
        return True
    def settle(self,key:str,actual_cents:int):
        if actual_cents<0:raise ValueError('negative actual cost')
        with sqlite3.connect(self.path,timeout=10) as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT cents,state FROM jobs WHERE key=?',(key,)).fetchone()
            if not row:raise KeyError(key)
            # Record an unexpected vendor overrun honestly, then block further spending.
            db.execute('UPDATE jobs SET cents=?,state=? WHERE key=?',(actual_cents,'settled',key))
            total=db.execute("SELECT COALESCE(SUM(cents),0) FROM jobs WHERE state!='released'").fetchone()[0]
        if total>self.limit:raise RuntimeError('vendor overrun recorded; production must pause')

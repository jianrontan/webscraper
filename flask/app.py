from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import datetime
import mysql.connector

app = Flask(__name__)

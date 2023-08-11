from flask import Flask, request, jsonify, send_from_directory, render_template, redirect, url_for, session, make_response, send_file
from datetime import datetime
import subprocess
import requests
import json
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret key'

DATABASE = 'nav.db'

# 显示所有导航
@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM nav_list")
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', navs=rows)

# 增加图片显示
@app.route('/static/images/<filename>')
def send_image(filename):
    return send_from_directory('./themes/webstack-hugo/static/assets/images/logos', filename)

# 添加导航
@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        logo = request.files['logo']
        url = request.form['url']
        description = request.form['description']
        term = request.form['term']
        taxonomy = request.form['taxonomy']
        icon = request.form['icon']

        # 保存图片
        logo.save(os.path.join('themes/webstack-hugo/static/assets/images/logos', logo.filename))
        # 保存到数据库
        logo = logo.filename
        print(logo)
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("INSERT INTO nav_list (title, logo, url, description, term, taxonomy, icon) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, logo, url, description, term, taxonomy, icon))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return render_template('add.html')
    
# 删除导航
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM nav_list WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 编辑导航
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        title = request.form['title']
        logo = request.files['logo']
        url = request.form['url']
        description = request.form['description']
        term = request.form['term']
        taxonomy = request.form['taxonomy']
        icon = request.form['icon']

# 判断是否有上传图片
        if logo.filename == '':
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("UPDATE nav_list SET title=?, url=?, description=?, term=?, taxonomy=?, icon=? WHERE id=?", (title, url, description, term, taxonomy, icon, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        else:
            # 保存图片
            logo.save(os.path.join('themes/webstack-hugo/static/assets/images/logos', logo.filename))
            # 保存到数据库
            logo = logo.filename
            print(logo)
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("UPDATE nav_list SET title=?, logo=?, url=?, description=?, term=?, taxonomy=?, icon=? WHERE id=?", (title, logo, url, description, term, taxonomy, icon, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    else:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT * FROM nav_list WHERE id=?", (id,))
        row = cur.fetchone()
        conn.close()
        return render_template('edit.html', nav=row)


# 上传git
@app.route('/execute', methods=['POST'])
def execute_command():
    if request.method == 'POST':
        # 执行 "go" 命令
        commit_message = 'Commit message here'

        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])
        return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5888)
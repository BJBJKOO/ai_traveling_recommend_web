import numpy as np
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import face_model, recommend_model, os


UPLOAD_FOLDER = 'static/image'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config['MYSQL_DATABASE_HOST'] = 'testdb.c4f6moxwyjbm.ap-northeast-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = '41693595'
app.config['MYSQL_DATABASE_DB'] = 'flask_DB'

mysql = MySQL()
mysql.init_app(app)

quests = []


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/quest_post", methods=['GET', 'POST'])
def quest_post():
    return render_template('quest_post.html')


@app.route("/image_post", methods=['GET', 'POST'])
def image_post():
    if request.method == "POST":
        quests.clear()
        for i in range(18):
            i = i + 1
            survay = 'survay' + str(i)
            try:
                quests.append(int(request.form.get(survay)))
            except:
                quests.append(request.form.get(survay))
        print(quests)
        return render_template('image_post.html')


@app.route("/recommend", methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        place_visit_prop = []
        placelist = []
        image_list = []
        tag_list = []
        url_list = []

        file_list = face_model.save_files(request, app.config['UPLOAD_FOLDER'])
        face_feeling = face_model.get_img_path(file_list)

        place_table = get_table()

        for place in place_table:
            placelist.append(place['place'])
            tag_list.append(place['tag'])
            url_list.append(place['URL'])

            input_data = quests \
                         + [float(place['theme_edu']), float(place['theme_act']), float(place['theme_nat'])] \
                         + [face_feeling]
            prop = recommend_model.recommend_place(input_data)
            place_visit_prop.append(prop)

        place_visit_prop = np.array(place_visit_prop)
        place_visit_top6 = np.flip(np.argpartition(place_visit_prop, -6)[-6:])

        tag_list = [tag_list[x].split(" ") for x in list(place_visit_top6)]
        url_list = [url_list[x] for x in list(place_visit_top6)]
        recommend_place = [placelist[x] for x in list(place_visit_top6)]
        for place in recommend_place:
            image_list.append('image/place/' + place + '.jpg')
        print(tag_list)
        return render_template('recommend_visit_list.html', image_list=image_list, place_list=recommend_place, tag_list=tag_list, url_list=url_list)


def get_table():
    cursor = mysql.get_db().cursor()
    cursor.execute('select * from travel_place_1')

    column_names = [x[0] for x in cursor.description]
    results = cursor.fetchall()
    place_list = []

    for result in results:
        place_list.append(dict(zip(column_names, result)))

    return place_list


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

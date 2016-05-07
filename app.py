import json
import operator
import os
from collections import OrderedDict

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from source.interface import Interface

interface = Interface(os.getcwd())
app = Flask(__name__, static_folder='resources', static_url_path='/assets')

UPLOAD_FOLDER = os.getcwd() + '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 0-5, 5-10, 10-15, 15-20, 20+
tempo_metric = [
    (0, 3),
    (3, 6),
    (6, 10),
    (10, 15),
    (15, 9999)
]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    tempo = request.form['tempo']
    actor_file = request.files['actor']
    scene_file = request.files['scene']

    # no scene, not allowed!!
    if not scene_file or not scene_file.filename:
        return jsonify(message='Please at least select one scene image'), 402

    if scene_file and scene_file.filename and allowed_file(scene_file.filename):
        filename = secure_filename(scene_file.filename)
        scene_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if actor_file and actor_file.filename and allowed_file(actor_file.filename):
        filename = secure_filename(actor_file.filename)
        actor_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    scene_descriptor = interface.get_scene_descriptor(
        os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(scene_file.filename)))

    all_scenes = interface.get_scene_data()

    scene_comp_ret = {}

    # key: clip name->movie_key
    # value: list of scene descriptor->[descriptor_1, descriptor_2, ...]
    for key, value in all_scenes.iteritems():
        cur_key_ret = 99999
        for one_des in value:
            temp = interface.compare_descriptor(scene_descriptor, one_des)
            if temp < cur_key_ret:
                cur_key_ret = temp
        scene_comp_ret[key] = cur_key_ret

    if actor_file and actor_file.filename:
        actor_descriptor = interface.get_face_descriptor(
            os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(actor_file.filename)), unique=True)
        all_actors = interface.get_actor_data()

        actor_comp_ret = {}
        for key, value in scene_comp_ret.iteritems():
            if all_actors.get(key) is None:
                continue
            for one_des in all_actors.get(key):
                temp = interface.compare_descriptor(actor_descriptor, one_des)
                if temp < 3.0:
                    actor_comp_ret[key] = value
                    break
        scene_comp_ret = actor_comp_ret

    if tempo is not None and tempo != '-1':
        down_metric, up_metric = tempo_metric[int(tempo)]
        all_tempos = interface.get_speed_data()
        pending_rm_keys = []
        for key, value in scene_comp_ret.iteritems():
            frame_num, t1, t2 = all_tempos[key]
            if (t1 + t2) <= down_metric or (t1 + t2) > up_metric:
                pending_rm_keys.append(key)
        for key in pending_rm_keys:
            del scene_comp_ret[key]

    temp_ret = OrderedDict(sorted(scene_comp_ret.items(), key=operator.itemgetter(1)))
    all_infos = interface.get_info_data()
    ret = OrderedDict()
    count = 1
    for key, value in temp_ret.iteritems():
        temp = {
            'cover_url': '/assets/' + os.path.relpath(interface.get_cover_for_event(key),
                                                      os.path.join(os.getcwd(), 'resources')),
            'url': '/assets/' + os.path.relpath(interface.get_clip_path(key), os.path.join(os.getcwd(), 'resources')),
            'fps': all_infos[key][0],
            'start': all_infos[key][1],
            'end': all_infos[key][2]
        }
        ret[key] = temp
        count += 1
        if count > 9:
            break

    return json.dumps(ret)


@app.route('/preview')
def preview():
    ret = []
    all_movies = interface.get_all_movie_names()
    for movie_name in all_movies:
        temp = {
            'cover_url': '/assets/' + os.path.relpath(interface.get_cover_for_movie(movie_name),
                                                      os.path.join(os.getcwd(), 'resources')),
            'url': '/assets/' + os.path.relpath(interface.get_raw_movie_path(movie_name),
                                                os.path.join(os.getcwd(), 'resources')),
            'name': movie_name
        }
        ret.append(temp)

    return render_template('preview.html', movies=ret)


@app.route('/clips/<movie_name>')
def clips(movie_name):
    ret = []
    all_clips = interface.get_all_keys(movie_name)
    for clip_name in all_clips:
        temp = {
            'cover_url': '/assets/' + os.path.relpath(interface.get_cover_for_event(clip_name),
                                                      os.path.join(os.getcwd(), 'resources')),
            'url': '/assets/' + os.path.relpath(interface.get_clip_path(clip_name),
                                                os.path.join(os.getcwd(), 'resources')),
            'name': clip_name
        }
        ret.append(temp)
    return render_template('clip_panel.html', clips=ret)


@app.route('/clip/<clip_name>')
def clip(clip_name):
    ret = {}
    all_faces = interface.get_face_paths(clip_name)
    all_scenes = interface.get_scene_paths(clip_name)

    ret['scene'] = []
    ret['face'] = []

    for face in all_faces:
        ret['face'].append('/assets/' + os.path.relpath(face, os.path.join(os.getcwd(), 'resources')))

    for scene in all_scenes:
        ret['scene'].append('/assets/' + os.path.relpath(scene, os.path.join(os.getcwd(), 'resources')))

    return render_template('scene_face.html', clip=ret)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

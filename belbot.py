#!/usr/bin/env python
import os
from flask import Flask, request, jsonify
import json
from random import shuffle

app = Flask(__name__)

GAME_ID = ''
FIRST_TURN = False
TRAINING = False

JUMPS = {
    '1': 0,
    '2': 1,
}

BOARD = {}


@app.route('/games', methods=['POST'])
def post_handler():
    print('[POST] /games')
    data = json.loads(request.data)

    global GAME_ID
    GAME_ID = data['id']
    global FIRST_TURN
    FIRST_TURN = data['first_turn']
    global TRAINING
    TRAINING = data['training']
    global JUMPS
    JUMPS = data['jumps']
    global BOARD
    BOARD = data['board']


    return jsonify(status='ok')


@app.route('/games/<string:id>', methods=['GET'])
def get_handler(id):
    print('[GET] games/:id')
    color = int(request.args.get('color'))
    cur_points = []

    for row_key, row in enumerate(BOARD['cells']):
        for col_key, col in enumerate(row):
            if BOARD['cells'][row_key][col_key] == color:
                cur_points.append([row_key, col_key])

    shuffle(cur_points)

    for cur_point in cur_points:
        row_key = cur_point[0]
        col_key = cur_point[1]

        even_params = [
            [row_key-1,col_key-1],
            [row_key-1,col_key],
            [row_key,col_key+1],
            [row_key+1,col_key-1],
            [row_key+1,col_key],
            [row_key,col_key-1],
        ]

        odd_params = [
            [row_key-1,col_key+1],
            [row_key-1,col_key],
            [row_key,col_key-1],
            [row_key+1,col_key+1],
            [row_key+1,col_key],
            [row_key,col_key+1],
        ]


        if row_key % 2 == 0:
            for param in even_params:
                try:
                    target_point = param

                    if BOARD['cells'][target_point[0]][target_point[1]] == 0\
                        and target_point[0] >= 0 and target_point[1] >= 0:
                        print "Its works"
                        return jsonify(
                            status='ok',
                            move_from=[cur_point[0], cur_point[1]],
                            move_to=[target_point[0], target_point[1]]
                        )
                except:
                    pass



        else:
            for param in odd_params:
                try:
                    target_point = param

                    if BOARD['cells'][target_point[0]][target_point[1]] == 0\
                        and target_point[0] >= 0 and target_point[1] >= 0:
                        print "Its works"
                        print [cur_point[0], cur_point[1]]
                        print [target_point[0], target_point[1]]
                        return jsonify(
                            status='ok',
                            move_from=[cur_point[0], cur_point[1]],
                            move_to=[target_point[0], target_point[1]]
                        )
                except:
                    pass

@app.route('/games/<string:id>', methods=['PUT'])
def put_handler(id):
    print('[PUT] games/:id')
    print(id)
    data = json.loads(request.data)

    global JUMPS
    JUMPS = data['jumps']
    changes = data['changes']

    for change in changes:
        print "OLD_BOARD"
        print BOARD['cells']
        print change
        global BOARD
        BOARD['cells'][change[0]][change[1]] = change[3]

    print(data)
    return jsonify(status='ok')


@app.route('/games/<string:id>', methods=['DELETE'])
def delete_handler(id):
    print('[DELETE] /games/:id')
    print(id)
    return jsonify(status='ok')


@app.route('/')
def index():
    print('root')
    return '.'


def main():
    port = int(os.environ.get('PORT', 8000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
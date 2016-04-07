import leap
import logging
from flask import Flask, jsonify

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
controller = leap.Controller()

def hand_state():
    frame = controller.frame()
    hands = frame.hands
    state = {'left': None, 'right': None}

    for hand in hands:
        if hand.is_valid:
            if hand.is_left:
                state['left'] = hand.palm_position.y
            elif hand.is_right:
                state['right'] = hand.palm_position.y

    return state

@app.route('/')
def api_root():
    return jsonify(hand_state())

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()

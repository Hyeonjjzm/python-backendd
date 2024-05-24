from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.posts = []
app.idCnt = 1

@app.route('/sign-up', methods=['POST'])
def signup():
    newUser = request.json
    newUser['id'] = app.idCnt
    app.users[app.idCnt] = newUser
    app.idCnt += 1
    return jsonify(newUser)

@app.route('/post', methods=['POST'])
def post():
    payload = request.json
    userID = int(payload['id'])
    msg = payload['msg']

    if userID not in app.users:
        return '사용자가 존재하지 않습니다', 400
    if len(msg) > 300:
        return '300자를 초과했습니다', 400

    app.posts.append({
        'user_id' : userID,
        'post' : msg
    })
    return '성공', 200

@app.route('/follow', methods=['post'])
def follow():
    payload = request.json
    userId = int(payload['id'])
    userIdToFollow = int(payload['follow'])
    
    if userId not in app.users or userIdToFollow not in app.users:
        return '사용자가 존재하지 않습니다', 400
    user = app.users[userId]
    if user.get('follow'):
        user['follow'].append(userIdToFollow)
        user['follow'] = list(set(user['follow']))
    else:
        user['follow'] = [userIdToFollow]
    return jsonify(user)

if __name__ == '__main__':
    app.run()
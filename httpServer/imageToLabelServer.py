from flask import request, Flask, render_template, jsonify
import ImageToLabel

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif', 'png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


imageToLabel = ImageToLabel.ImageToLabel()


@app.route('/image_to_label', methods=['POST'])
def image_to_label():
    """
    上传验证码文件 获取验证码字符串
    文件字段
    :return: 一个识别后的验证码字符串
    """
    if not 'captcha' in request.files:
        return jsonify({'code': -1, 'message': '请上传验证码文件'})
    captcha_file = request.files['captcha']
    if captcha_file and allowed_file(captcha_file.filename):
        captcha_bytes = captcha_file.read()
        return jsonify({'code': 1, 'captcha_label': imageToLabel.getImageLabel(captcha_bytes)})
    else:
        return jsonify({'code': -1, 'message': '验证码文件有误'})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

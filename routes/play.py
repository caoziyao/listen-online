from models.play import Playlist
from routes import *


main = Blueprint('play', __name__)


@main.route('/')
def index():
    # ts = Todo.query.all()
    # return render_template('todo_index.html', todo_list=ts)
    return 'Hello'


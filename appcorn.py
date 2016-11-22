# nohup gunicorn -w4 -b0.0.0.0:80 appcorn:application &

from app import configured_app
# from app import configure_manager
# from app import manager

application = configured_app()

# if __name__ == '__main__':
#     configure_manager()
#     application
#     manager.run()       # 命令行
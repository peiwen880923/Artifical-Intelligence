'''
   movie_inf 使用範例
'''

from movie_inf import *

if __name__ == '__main__':
    movie_name = input()
    movie = movie_inf(movie_name)
    
    print("電影資訊")
    print(movie.get_movie_inf())
    print("演員名單")
    print(movie.get_actor())
    print("預告片連結")
    print(movie.get_video_link())
    print("星級")
    print(movie.get_star())
    print("爛番茄指數")
    print(movie.get_tomato())
    print("電影評論")
    print(movie.get_comment())
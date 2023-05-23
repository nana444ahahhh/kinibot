from urllib.request import urlopen

resource = urlopen('https://avatars.mds.yandex.net/get-ott/223007/2a00000171876d43e075f5a17c706c17435f/orig')
out = open("img.jpg", 'wb')
out.write(resource.read())
out.close()

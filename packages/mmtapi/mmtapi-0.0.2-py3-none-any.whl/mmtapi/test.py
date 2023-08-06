import os, json, requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def main():

    token = '0f3732fcfb1c8577c390e71a176f3c8f'
    catalogid = 486
    targetid = 6302
    programid = 977
    url = 'https://scheduler.mmto.arizona.edu/upload.php'
    finder = 'M51.jpg'

    multipart_data = MultipartEncoder(
        fields={
            'finding_chart_file':(finder, open(finder, 'rb').read(), 'image/jpeg'),
            'type':'finding_chart',
            'token':token,
            'catalog_id':str(catalogid),
            'program_id':str(programid),
            'target_id':str(targetid),
        }
    )

    headers = {
        'Content-Type':multipart_data.content_type,
        'User-Agent':'Mozilla/5.0'
    }

    r = requests.post(url, headers=headers, data=multipart_data)
    print(r.text)

main()

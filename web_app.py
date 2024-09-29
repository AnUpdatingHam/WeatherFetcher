from flask import *
from constant import *
import weather_mapper
import weather_graph_generator

app = Flask(__name__)

@app.route('/')
def home():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>主页</title>
        <style>
            body {
                background-image: url('https://img2.baidu.com/it/u=3525305620,4229839045&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=500');
                background-size: cover;
                font-family: Arial, sans-serif;
            }
            .container {
                width: 50%;
                height:100%;
                margin: auto;
                padding-top: 10%;
            }
            .content{
                padding-top: 15%;
                height:100%;
                padding-left: 20%;
            }
            h1 {
                color: white;
                text-align: center;
                font-size: 50px
            }
            .button {
                display: block;
                width: 150px;
                margin: 20px auto;
                padding: 10px;
                font-size: 16px;
                color: white;
                background-color: #007bff;
                border: none;
                border-radius: 10px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>福建省天气查询应用</h1>
            <div class="content">
            <form action="/map" method="post">
                <button type="submit" class="button">福建省气温分布图</button>
            </form>
            <form action="/weather" method="post">
                <label for="city">选择城市：</label>
                <select name="city" id="city">
                '''
    for eng_city_name, chi_city_name in chinese_fujian_cities_names.items():
        html_content += f'''
                    <option value="{chi_city_name}">{chi_city_name}</option>
                '''
    html_content += '''
                </select>
                <button type="submit" class="button">查询天气</button>
            </form>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)



@app.route('/weather', methods=['POST'])
def weather_view():
    chi_city_name = request.form.get('city')
    if chi_city_name:
        data = weather_mapper.get_data(english_fujian_cities_names[chi_city_name])

        # 将数据转换为HTML表格
        html_table = "<table border='1'>\n"
        html_table += "<tr><th>城市</th><th>日期</th><th>最高温度</th><th>最低温度</th><th>天气类型</th><th>风向风力</th></tr>\n"

        for row in data:
            eng_city_name, date, highest_temp, lowest_temp, weather_type, wind = row
            html_table += f"<tr>\n"
            html_table += f"<td>{chi_city_name}</td>\n"
            html_table += f"<td>{date}</td>\n"
            html_table += f"<td>{highest_temp}</td>\n"
            html_table += f"<td>{lowest_temp}</td>\n"
            html_table += f"<td>{weather_type}</td>\n"
            html_table += f"<td>{wind}</td>\n"
            html_table += "</tr>\n"

        html_table += "</table>"

        # 使用render_template_string渲染HTML表格
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{chi_city_name}7月天气历史记录</title>
            <style>
                table, th, td {{
                    border: 1px solid black;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            <h1>{chi_city_name}7月天气历史记录</h1>
            {html_table}
        </body>
        </html>
        """
        return render_template_string(html_content)
    else:
        # 如果没有选择城市，返回错误信息或提示
        return '请选择一个城市', 400


@app.route('/map', methods=['POST'])
def map_view():
    return weather_graph_generator.get_html()


if __name__ == '__main__':
    app.run(debug=True)


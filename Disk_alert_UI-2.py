import logging
import os
import json
import smtplib
import redis
import traceback

from datetime import timedelta, datetime, date
from inspect import cleandoc
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

level = "DEBUG"
logging.basicConfig(level=level, format="%(levelname)-10s| %(asctime)-10s | %(funcName)-10s | %(message)s")


EMAIL_FROM_ID = "from_user@gmail.com"
EMAIL_TO_IDS = ["to_user@gmail.com", ]
SMTP_USER_NAME = "user@gmail.com"
SMTP_USER_PASS = "userpwd"


def get_cur_date_time():
    return datetime.now().strftime("%Y%m%d - %H:%M:%S")


def generate_email():
    """Returns template"""
    template = cleandoc("""
        <html lang="en">
<head>
  <title>Mail</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <style>
  table
  {
    border:1px solid black;
    border-collapse:collapse ;
    padding:0px;
  }
  th
  {
    padding:10px;
    border:1px solid black;
  }
  td
  {
    padding:10px;
    border:1px solid black;
    text-align:left;
  }
  tbody >tr:nth-child(even)
  {
    background-color:white;
  }
  tbody >tr:nth-child(odd)
  {
    background-color:#eee;
  }
  .table>thead>tr>th
  {
    vertical-align: bottom;
    border-bottom: 1px solid black;
    text-align: center;
  }
  .table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th {
    padding: 10px;
    line-height: 1.42857143;
    vertical-align: top;
    border-top: 1px solid #ddd;
  }
  .please_look .progress-bar
  {
    background-color: #337ab7 !important;
  }
  .normal .progress-bar
  {
    background-color: #5cb85c !important;
  }
  .super_critical .progress-bar
  {
    background-color: #ac2925 !important;
  }
  .progress
  {
    border: 1px solid black;
    height: 20px;
    margin-bottom: 20px;
    overflow: hidden;
    background-color: #f5f5f5;
    border-radius: 4px;
  }
  .progress-bar {
    float: left;
    height: 100%;
    font-size: 12px;
    line-height: 20px;
    color: #fff;
    text-align: center;
    box-shadow: inset 0 -1px 0 rgba(0,0,0,.15);
    transition: width .6s ease;
    }
  </style>
</head>
<body>
<div class="container">
  <h2><center>Disk Usage Reports</center></h2>
  <p><center><b>Report Generated at 20181116 - 06:31:30</b></center></p>
  <center>
  <table class="table">
    <thead style="background-color:#32A9EE;color:white">
      <tr>
        <th style="border-top:1px solid black"><b>Node Name</b></th>
        <th style="border-top:1px solid black"><b>Mount Point</b></th>
        <th style="border-top:1px solid black"><b>Total Size</b></th>
        <th style="border-top:1px solid black"><b>Used Size</b></th>
        <th style="border-top:1px solid black"><b>Free Size</b></th>
        <th style="border-top:1px solid black"><b>Percentage Indicator</b></th>
        <th style="border-top:1px solid black"><b>Critical Level</b></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>dvwhk-jenkins ( <i>rdansible@10.40.51.62</i> )</b></td>
        <td><b>/</b></td>
        <td><b>263.1 GB</b></td>
        <td><b>211.5 GB</b></td>
        <td><b>38.2 GB</b></td>
        <td>
          <div class="progress please_look">
            <div class="progress-bar" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" style="width:85%">85%</div>
          </div>
        </td>
        <td><b>Please look</b></td>
      </tr>
      <tr>
        <td><b>dvserver6 ( <i>rdansible@10.40.51.6</i> )</b></td>
        <td><b>/</b></td>
        <td><b>257.6 GB</b></td>
        <td><b>182.3 GB</b></td>
        <td><b>62.3 GB</b></td>
        <td>
          <div class="progress normal">
            <div class="progress-bar" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width:75%">75%</div>
          </div>
        </td>
        <td><b>Normal</b></td>
      </tr>
      <tr>
        <td><b>dvserver5 ( <i>rdansible@10.40.51.5</i> )</b></td>
        <td><b>/</b></td>
        <td><b>257.6 GB</b></td>
        <td><b>238.3 GB</b></td>
        <td><b>6.2 GB</b></td>
        <td>
          <div class="progress super_critical">
            <div class="progress-bar" role="progressbar" aria-valuenow="98" aria-valuemin="0" aria-valuemax="100" style="width:98%">98%</div>
          </div>
        </td>
        <td><b>Super Critical</b></td>
      </tr>
      <tr>
        <td><b>server27 ( <i>rdansible@10.40.51.27</i> )</b></td>
        <td><b>/</b></td>
        <td><b>257.6 GB</b></td>
        <td><b>147.6 GB</b></td>
        <td><b>96.9 GB</b></td>
        <td>
          <div class="progress normal">
            <div class="progress-bar" role="progressbar" aria-valuenow="61" aria-valuemin="0" aria-valuemax="100" style="width:61%">61%</div>
          </div>
        </td>
        <td><b>Normal</b></td>
      </tr>
      <tr>
        <td><b>dvserver12 ( <i>rdansible@10.40.51.12</i> )</b></td>
        <td><b>/</b></td>
        <td><b>257.6 GB</b></td>
        <td><b>207.0 GB</b></td>
        <td><b>37.5 GB</b></td>
        <td>
          <div class="progress please_look">
            <div class="progress-bar" role="progressbar" aria-valuenow="85" aria-valuemin="0" aria-valuemax="100" style="width:85%">85%</div>
          </div>
        </td>
        <td><b>Please look</b></td>
      </tr>
      <tr>
        <td><b>WIN-7U3C8GAPDJI ( <i>Administrator@10.9.141.23</i> )</b></td>
        <td><b>C:</b></td>
        <td><b>465.2 GB</b></td>
        <td><b>328.9 GB</b></td>
        <td><b>136.3 GB</b></td>
        <td>
          <div class="progress normal">
            <div class="progress-bar" role="progressbar" aria-valuenow="70.7" aria-valuemin="0" aria-valuemax="100" style="width:70.7%">70.7%</div>
          </div>
        </td>
        <td><b>Normal</b></td>
      </tr>
    </tbody>
  </table>
  </center>
</div>
</body>
</html>



    """)
    return Template(cleandoc(template))


def mail_alert(subject, send_to, send_from, body):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to)

    msg.attach(MIMEText(body, 'html'))

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(SMTP_USER_NAME, SMTP_USER_PASS)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    pdata = [{'LoginName': u'rdansible', 'DiskUsageIndicator': {'msg': 'Please look', 'colour': 'RoyalBlue'},
              'TotalSize': '263.1 GB', 'IpAddress': u'10.40.51.62', 'HostName': u'dvwhk-jenkins',
              'UsedSize': '211.5 GB', 'UsedPctBar': {'high': 170.0, 'low': 30.0}, 'FreePct': u'14.5', 'UsedPct': u'85',
              'MountPoint': u'/', 'NoRecords': 1, 'FreeSize': '38.2 GB'}]

    output_from_parsed_template = generate_email().render(
        data=pdata,
        cur_date_time=get_cur_date_time
    )
    mail_alert(
        subject="Disk alert",
        send_to=EMAIL_TO_IDS,
        send_from=EMAIL_FROM_ID,
        body=output_from_parsed_template
    )
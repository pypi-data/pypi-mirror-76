import unittest
import nightscout
from datetime import datetime
from dateutil.tz import tzutc
from httmock import all_requests, HTTMock
import pytz


@all_requests
def sgv_response(url, request):
    return '[{"_id":"5f2b01f5c3d0ac7c4090e223","device":"xDrip-LimiTTer","date":1596654066533,"dateString":"2020-08-05T19:01:06.533Z","sgv":169,"delta":-5.257,"direction":"FortyFiveDown","type":"sgv","filtered":182823.5157,"unfiltered":182823.5157,"rssi":100,"noise":1,"sysTime":"2020-08-05T19:01:06.533Z","utcOffset":-180},{"_id":"5f2b00c8c3d0ac7c4090e222","device":"xDrip-LimiTTer","date":1596653766048,"dateString":"2020-08-05T18:56:06.048Z","sgv":174,"delta":-2.028,"direction":"Flat","type":"sgv","filtered":187411.75065,"unfiltered":187411.75065,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:56:06.048Z","utcOffset":-180},{"_id":"5f2aff9dc3d0ac7c4090e221","device":"xDrip-LimiTTer","date":1596653466421,"dateString":"2020-08-05T18:51:06.421Z","sgv":176,"delta":-5.66,"direction":"FortyFiveDown","type":"sgv","filtered":189176.4564,"unfiltered":189176.4564,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:51:06.421Z","utcOffset":-180},{"_id":"5f2afe70c3d0ac7c4090e220","device":"xDrip-LimiTTer","date":1596653165840,"dateString":"2020-08-05T18:46:05.840Z","sgv":182,"delta":-2.97,"direction":"Flat","type":"sgv","filtered":194117.63249999998,"unfiltered":194117.63249999998,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:46:05.840Z","utcOffset":-180},{"_id":"5f2afd44c3d0ac7c4090e21f","device":"xDrip-LimiTTer","date":1596652865845,"dateString":"2020-08-05T18:41:05.845Z","sgv":185,"delta":-5.946,"direction":"FortyFiveDown","type":"sgv","filtered":196705.8676,"unfiltered":196705.8676,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:41:05.845Z","utcOffset":-180},{"_id":"5f2afc18c3d0ac7c4090e21e","device":"xDrip-LimiTTer","date":1596652566127,"dateString":"2020-08-05T18:36:06.127Z","sgv":191,"delta":-5.772,"direction":"FortyFiveDown","type":"sgv","filtered":201882.33779999998,"unfiltered":201882.33779999998,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:36:06.127Z","utcOffset":-180},{"_id":"5f2afa42c3d0ac7c4090e21d","device":"xDrip-LimiTTer","date":1596652095925,"dateString":"2020-08-05T18:28:15.925Z","sgv":200,"delta":-3.51,"direction":"Flat","type":"sgv","filtered":209764.69014999998,"unfiltered":209764.69014999998,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:28:15.925Z","utcOffset":-180},{"_id":"5f2af916c3d0ac7c4090e21c","device":"xDrip-LimiTTer","date":1596651795916,"dateString":"2020-08-05T18:23:15.916Z","sgv":203,"delta":-5.4,"direction":"FortyFiveDown","type":"sgv","filtered":212823.51345,"unfiltered":212823.51345,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:23:15.916Z","utcOffset":-180},{"_id":"5f2af7eac3d0ac7c4090e21b","device":"xDrip-LimiTTer","date":1596651495909,"dateString":"2020-08-05T18:18:15.909Z","sgv":209,"delta":2.702,"direction":"Flat","type":"sgv","filtered":217529.39544999998,"unfiltered":217529.39544999998,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:18:15.909Z","utcOffset":-180},{"_id":"5f2af6bec3d0ac7c4090e21a","device":"xDrip-LimiTTer","date":1596651196104,"dateString":"2020-08-05T18:13:16.104Z","sgv":206,"delta":-4.454,"direction":"Flat","type":"sgv","filtered":215176.45445,"unfiltered":215176.45445,"rssi":100,"noise":1,"sysTime":"2020-08-05T18:13:16.104Z","utcOffset":-180}]'


def treatments_response(url, request):
    return '[{"_id":"58be816483ab6d6632419686","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:38:35Z","timestamp":"2017-03-07T09:38:35Z","absolute":0.7,"rate":0.7,"duration":30,"carbs":null,"insulin":null},{"_id":"58be803d83ab6d6632419683","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:33:30Z","timestamp":"2017-03-07T09:33:30Z","absolute":1.675,"rate":1.675,"duration":30,"carbs":null,"insulin":null},{"_id":"58be7f0d83ab6d6632419680","temp":"absolute","enteredBy":"loop://Riley\'s iphone","eventType":"Temp Basal","created_at":"2017-03-07T09:28:30Z","timestamp":"2017-03-07T09:28:30Z","absolute":1.775,"rate":1.775,"duration":30,"carbs":null,"insulin":null}]'


def profile_response(url, request):
    return '[{"_id":"58c0e02447d5af0c00e37593","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.4","timeAsSeconds":"61200"},{"time":"20:30","value":"0.4","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"},"Test2":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.4","timeAsSeconds":"61200"},{"time":"20:30","value":"0.4","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2017-03-24T03:54:00.000Z","mills":"1489035240000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"},{"_id":"58b7777cdfb94b0c00366c7e","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"20","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.6","timeAsSeconds":"61200"},{"time":"20:30","value":"0.6","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2017-03-02T01:37:00.000Z","mills":"1488418620000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"},{"_id":"5719b2aa5c3e080b000dbfb1","defaultProfile":"Default","store":{"Default":{"dia":"4","carbratio":[{"time":"00:00","value":"18","timeAsSeconds":"0"},{"time":"06:00","value":"10","timeAsSeconds":"21600"},{"time":"11:00","value":"18","timeAsSeconds":"39600"},{"time":"16:00","value":"12","timeAsSeconds":"57600"},{"time":"21:00","value":"18","timeAsSeconds":"75600"}],"carbs_hr":"20","delay":"20","sens":[{"time":"00:00","value":"90","timeAsSeconds":"0"},{"time":"06:00","value":"85","timeAsSeconds":"21600"},{"time":"09:00","value":"95","timeAsSeconds":"32400"}],"timezone":"US/Central","basal":[{"time":"00:00","value":"0.45","timeAsSeconds":"0"},{"time":"02:00","value":"0.3","timeAsSeconds":"7200"},{"time":"04:30","value":"0.45","timeAsSeconds":"16200"},{"time":"07:00","value":"0.6","timeAsSeconds":"25200"},{"time":"10:00","value":"0.4","timeAsSeconds":"36000"},{"time":"12:00","value":"0.4","timeAsSeconds":"43200"},{"time":"15:00","value":"0.4","timeAsSeconds":"54000"},{"time":"17:00","value":"0.6","timeAsSeconds":"61200"},{"time":"20:30","value":"0.6","timeAsSeconds":"73800"}],"target_low":[{"time":"00:00","value":"110","timeAsSeconds":"0"}],"target_high":[{"time":"00:00","value":"130","timeAsSeconds":"0"}],"startDate":"1970-01-01T00:00:00.000Z","units":"mg/dl"}},"startDate":"2016-04-22T05:06:00.000Z","mills":"1461301560000","units":"mg/dl","created_at":"2016-10-31T12:58:43.800Z"}]'


def server_status_response(url, request):
    return '{"status":"ok","name":"nightscout","version":"13.0.1","serverTime":"2020-08-05T18:14:02.032Z","serverTimeEpoch":1596651242032,"apiEnabled":true,"careportalEnabled":true,"boluscalcEnabled":true,"settings":{"units":"mg/dl","timeFormat":12,"nightMode":false,"editMode":true,"showRawbg":"never","customTitle":"Nightscout","theme":"default","alarmUrgentHigh":true,"alarmUrgentHighMins":[30,60,90,120],"alarmHigh":true,"alarmHighMins":[30,60,90,120],"alarmLow":true,"alarmLowMins":[15,30,45,60],"alarmUrgentLow":true,"alarmUrgentLowMins":[15,30,45],"alarmUrgentMins":[30,60,90,120],"alarmWarnMins":[30,60,90,120],"alarmTimeagoWarn":true,"alarmTimeagoWarnMins":15,"alarmTimeagoUrgent":true,"alarmTimeagoUrgentMins":30,"alarmPumpBatteryLow":false,"language":"en","scaleY":"log","showPlugins":" delta direction upbat","showForecast":"ar2","focusHours":3,"heartbeat":60,"baseURL":"","authDefaultRoles":"readable","thresholds":{"bgHigh":260,"bgTargetTop":180,"bgTargetBottom":80,"bgLow":55},"insecureUseHttp":false,"secureHstsHeader":true,"secureHstsHeaderIncludeSubdomains":false,"secureHstsHeaderPreload":false,"secureCsp":false,"deNormalizeDates":false,"showClockDelta":false,"showClockLastTime":false,"DEFAULT_FEATURES":["bgnow","delta","direction","timeago","devicestatus","upbat","errorcodes","profile"],"alarmTypes":["predict"],"enable":["careportal","boluscalc","food","bwp","cage","sage","iage","iob","cob","basal","ar2","rawbg","pushover","bgi","pump","openaps","treatmentnotify","bgnow","delta","direction","timeago","devicestatus","upbat","errorcodes","profile","ar2"]},"extendedSettings":{"devicestatus":{"advanced":true}},"authorized":null}'


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = nightscout.Api("http://testns.example.com")

    def test_get_sgv(self):
        with HTTMock(sgv_response):
            entries = self.api.get_sgvs()

        self.assertEqual(10, len(entries))
        self.assertEqual(169, entries[0].sgv)
        self.assertEqual("FortyFiveDown", entries[0].direction)
        self.assertEqual(-5.257, entries[0].delta)
        self.assertEqual(
            datetime(2020, 8, 5, 19, 1, 6, 533000, tzinfo=tzutc()), entries[0].date
        )

    def test_get_treatments(self):
        with HTTMock(treatments_response):
            treatments = self.api.get_treatments()

        self.assertEqual(3, len(treatments))
        self.assertEqual("absolute", treatments[0].temp)
        self.assertEqual("Temp Basal", treatments[0].eventType)
        timestamp = datetime(2017, 3, 7, 9, 38, 35, tzinfo=tzutc())
        self.assertEqual(timestamp, treatments[0].timestamp)
        self.assertEqual(timestamp, treatments[0].created_at)

    def test_get_profile(self):
        with HTTMock(profile_response):
            profile_definition_set = self.api.get_profiles()

        profile_definition = profile_definition_set.get_profile_definition_active_at(
            datetime(2017, 3, 5, 0, 0, tzinfo=tzutc())
        )
        self.assertEqual(
            datetime(2017, 3, 2, 1, 37, tzinfo=tzutc()), profile_definition.startDate
        )
        self.assertEqual("mg/dl", profile_definition.units)

        profile = profile_definition.get_default_profile()
        self.assertEqual(pytz.timezone("US/Central"), profile.timezone)
        self.assertEqual(4, profile.dia)

        five_thirty_pm = datetime(2017, 3, 24, 17, 30)
        five_thirty_pm = profile.timezone.localize(five_thirty_pm)
        self.assertEqual(0.6, profile.basal.value_at_date(five_thirty_pm))

    def test_server_status(self):
        with HTTMock(server_status_response):
            server_status = self.api.get_server_status()

        self.assertEqual("ok", server_status.status)
        self.assertEqual("nightscout", server_status.name)
        self.assertEqual(True, server_status.apiEnabled)


if __name__ == "__main__":
    unittest.main()

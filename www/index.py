#!/usr/bin/python
import sys

from inc import web
from inc.helper import Convert
from inc.Config import Config

sys.stderr = sys.stdout 


def main():
	#print LocalConfig.Global.TestName
	http = web.Output()
	http.Begin()

	http.Print("<!DOCTYPE html>")
	http.Print("<html>")
	http.Print("<head>")
	http.Indent(1)
	http.Print("<title>Weather</title>")
	http.Print("<link rel='stylesheet' href='./css/weather.css' type='text/css' media='all' />")
	http.Print("<script src='./jquery/jquery.min.js'></script>")
	http.Print("<script src='./js/moment.js'></script>")
	http.Print("<script src='./js/weather.js'></script>")
	http.Outdent(1)
	http.Print("</head>")
	http.Print("<body>")
	http.Print("<div id='Toaster'><!-- Toast Message Placeholder Container --></div>")
	http.Indent(1)
	http.Print("<div id='container'>")
	http.Indent(1)
	http.Print("<div id='radar'>")
	http.Indent(1)
	http.Print("<div id='topBar'>")
	http.Print("<select id='RadarSelect'></select>")
	http.Print("<select id='SiteSelect'></select>")
	http.Print("<div><a href='#' id='refreshData'>REFRESH</a></div>")
	http.Print("<div><h1 class='ConditionCaption'></h1><h2 data-linkfield='warn' class='CondAlerts UpdatableField' id='condAlertWarn'>0</h2><h2 data-linkfield='watch' class='CondAlerts UpdatableField' id='condAlertWatch'>0</h2><h2 data-linkfield='other' class='CondAlerts UpdatableField' id='condAlertOther'>0</h2></div>")
	http.Print("<div><h1 class='ConditionCaption'></h1><h2 class='ConditionValue UpdatableField' id='condTime'>00:00 EST</h2></div>")
	http.Print("<div><h1 class='ConditionCaption DivBar'>Cond:</h1><h2 class='ConditionValue UpdatableField' id='condCurrent'>Raining</h2></div>")
	http.Print("<div><h1 class='ConditionCaption DivBar'>Temp:</h1><h2 class='ConditionValue UpdatableField' id='condTemp'>?</h2></div>")
	http.Print("<div><h1 class='ConditionCaption DivBar'>Feels: </h1><h2 class='ConditionValue UpdatableField' id='condFeels'>?</h2></div>")
	http.Print("<div><h1 class='ConditionCaption DivBar'>Wind: </h1><h2 class='ConditionValue UpdatableField' id='condWind'>?</h2></div>")
	http.Print("<div><a href='#' id='detailsDataClick'>&#9660;</a></div>")
	http.Outdent(1)
	http.Print("</div>")
	http.Print("<div class='trap' id='alertPopup'><div id='w'>content</div></div>")
	http.Print("<div class='foldDown' id='detailsPopup'>")
	http.Indent(1)
	http.Print("<div class='detailsHeader' id='condSiteName'>City Name</div>")
	http.Print("<div class='detailsColumn'>")
	http.Print("<div class='detailsItemCaption'>Pressure:</div><div class='detailsItemValue UpdatableField' id='condPressure'>--</div>")
	http.Print("<div class='detailsItemCaption'>Relative Humidity:</div><div class='detailsItemValue UpdatableField' id='condRH'>--</div>")
	http.Print("<div class='detailsItemCaption'>Dew Point:</div><div class='detailsItemValue UpdatableField' id='condDewPoint'>--</div>")
	http.Print("<div class='detailsItemCaption'>Visiblity:</div><div class='detailsItemValue UpdatableField' id='condVis'>--</div>")
	http.Print("</div>")
	http.Print("<div class='detailsColumn'>.</div>")
	http.Outdent(1)
	http.Print("</div>")
	http.Print("<img id='radarimg' src='./loading.jpeg' />")
	http.Print("</div>")
	http.Outdent(1)
	http.Print("</div>")
	http.Outdent(1)
	http.Print("\n</body>")
	http.Print("</html>")

	http.Finish()


#Run main
if __name__ == '__main__':
	main()

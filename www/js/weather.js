var RadarSources = Array();
RadarSources[0] = {"Url": "./img/loading.jpeg", "Caption": "Loading"};
RadarSources[1] = {"Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=70&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile", "Caption": "WunderMap - N0R - Wide"};
RadarSources[2] = {"Url": "http://radblast.wunderground.com/cgi-bin/radar/WUNIDS_composite?centerlat=43.33.2&centerlon=-79.82&radius=20&type=N0R&num=1&delay=50&width=[w]&height=[h]&newmaps=1&smooth=1&showstorms=0&showlabels=1&lightning=1&brand=mobile", "Caption": "WunderMap - N0R - Local"};

var AlertData;
var DataCache;
var Config;

//Toast stuff
var ToastCounter = 0;
var ToastTypes = {
    ERROR: 0,
    WARNING: 1,
    INFO: 2
};


var CurrentState = {
	"InitialPageWidth": 0,
	"InitialPageHeight": 0,
	"RadarSite": 0,
	"DataSite": 0
}

function Main()
{
	CurrentState.InitialPageWidth = $(window).width()-3;
	CurrentState.InitialPageHeight = $(window).height()-3;
	
	//Set defaults
    SetRadarImages();
    SetSiteLists();
    LoadRadarImage(0);
    LoadSiteData(0);
    
    //Add click handlers
  	
  	//Data refresh click handler
  	$("#refreshData").click(function() {
    	//Refresh radar
    	LoadRadarImage(CurrentState.RadarSite);
    	LoadSiteData(CurrentState.DataSite);
    	
    });
    
    //Details expand click handler
    $("#detailsDataClick").click(
    	function() 
    	{
    		 
    		$("#detailsPopup").fadeToggle(250, function() 
    		{
    		 	var isVisible = $( this ).is( ":visible" );
    		 	if (isVisible == true)
    		 	{
					$("#detailsDataClick").html("&#9650;");
    		 	}
    		 	else
    		 	{
					$("#detailsDataClick").html("&#9660;");
				}
    		});

    	}
    );
    
    //Alerts display click handler
    $(".CondAlerts").click(
    	function() 
    	{
    		 
    		//var currentLeft = $( this ).position("left");
    		var currentBgColor = $( this ).css("background-color");
    		var alertType = $(this).data("linkfield");
    		$("#alertPopup").fadeToggle(1, function() 
    		{
    		 	
    		 	var isVisible = $( this ).is( ":visible" );
    		 	if (isVisible == true)
    		 	{
    		 		$("#alertPopup").css("background-color", currentBgColor);
    		 		LoadAlertData(alertType);
    		 	}
    		});

    	}
    );
}

//Gets executed once the document ready is called.
function PreMain()
{
	//Load the config object
	$.ajax(
		{
			url: './inc/Ajax.GetSettings.py',
			success: function (result)
			{
				//Load remote config
				Config = JSON.parse(result);
				//Continue to main
				Main();
			}	
		}
	)
	;
}


//Show error messages on screen
function ShowError(message, type)
{
	//Inc the counter, this allows us to have unique ID's for each message,
	//which is needed for correct selection and closing of the messages
	ToastCounter++;
	
	//Create the new ID
	var newId = "Toast" + ToastCounter.toString();
	//Container to place them in
	var baseTo = $('#Toaster');
	//Default warnign class type
	var colorType = "ToastInfo";
	
	//Pick the correct color based on type
	if (type == ToastTypes.ERROR)
		colorType = "ToastError";
	else if (type == ToastTypes.WARNING)
		colorType = "ToastWarning";
	
	//Use this template for new items
	var template = "<div id='ToastPopup' class='ToastTemplate'><div class='ToastCloseButton'><a href='#'>X</a></div><h2>Message</h2></div>";
	$(template).clone().attr('id', newId).appendTo(baseTo);
	//set the message
	$("#" + newId + " h2").html(message);
	//set the color
	$("#" + newId + "").addClass(colorType);
	//fade it on the screen
	$("#" + newId).fadeIn(200);
	//add the close button click event
	$("#" + newId + " .ToastCloseButton a").click(function () {
		$("#" + newId).fadeOut(200);
	});
}

function ProcessJSON(result)
{
	//Parse the JSON result into a object
	try
	{
		j = JSON.parse(result);
	}
	catch (ex)
	{
		//Check if we get response starting with "Traceback", as this is actually a Python error
		if (result.indexOf("Traceback") != -1)
		{
			ShowError("Server: Python traceback error!<br/><br/><code><b>Response:</b><br/>" + result + "</code>",  ToastTypes.ERROR);
			return;
		}
		else
		{
			ShowError("Local: JSON parse to object error!<br/><br/><code><b>Response:</b><br/>" + result + "</code>",  ToastTypes.ERROR);
			return;
		}
	}
	
	//Check for an returned error
	if (j.status == "failure")
	{
		ShowError("Remote Error:\n\n" + j.errorMsg, ToastTypes.ERROR);
		return;
	}
	else if (j.status == "success")
	{
		//Do nothing
	}
	else
	{
		alert("Invalid response:\n\n" + result);
		return;
	}
	
	//Save data to global var
	DataCache = j;
	
	


}

//Actually updat the page elements
function UpdatePageElements()
{
	//Current alerts
	$("#condAlertWarn").html(DataCache.alerts.counts.warnings.toString());
	$("#condAlertWatch").html(DataCache.alerts.counts.watches.toString());
	$("#condAlertOther").html(DataCache.alerts.counts.statements.toString());
	
	//The observation time
	var obDateTime = new Date(DataCache.currentConditions.ObservationDateTime );
	var obDateTimeString = moment(obDateTime).format("hh:MM A");
	$("#condTime").html(obDateTimeString);
	
	//Station name
	$("#condSiteName").html(DataCache.currentConditions.StationName);
	
	//Conditions
	$("#condCurrent").html(DataCache.currentConditions.Conditions);
	
	//Temp
	$("#condTemp").html(DataCache.currentConditions.Temperature + " &deg;C");
	
	//Feels like - Windchill/Humidex, if present
	if (DataCache.currentConditions.Feels == null)
		$("#condFeels").html("N/A");
	else
		$("#condFeels").html(DataCache.currentConditions.Feels + "");
	
	//Wind
	var windDirString = "";
	var windGustString = "";
	var windString = "";
	//If there is wind direction
	if (DataCache.currentConditions.WindDirection != -1)
	{
		windDirString = "" + toCardinalDir(DataCache.currentConditions.WindDirection);
		//If there is gust data present
		if (DataCache.currentConditions.WindGust != -1)
			windGustString = " (G: " + DataCache.currentConditions.WindGust.toString() + ")	";
		else
			windGustString = "";
	}
	
	//If there is wind speed
	if (DataCache.currentConditions.WindSpeed > 0)
		var windString = DataCache.currentConditions.WindSpeed.toString() + " km/h @ " + windDirString + " " + windGustString
	else
		var windString = "No Wind";
		
	$("#condWind").html(windString);
	
	$("#condDewPoint").html(DataCache.currentConditions.DewPoint.toString() + " &deg;C");
	
	//Pressure
	$("#condPressure").html(DataCache.currentConditions.Pressure.toString() + " kPa (" + DataCache.currentConditions.PressureChange.toString() + ")");
	
	//RH
	$("#condRH").html(DataCache.currentConditions.RelativeHumidity.toString() + " %");
	
	//Visibility
	$("#condVis").html(DataCache.currentConditions.Visibility.toString() + " km");
	
	
}

function UpdateSiteData(ajaxUrl)
{
		//alert('f');
		//Update all the data fields
		//Once all updatable fields have hidden, then do the ajax call
		$(".UpdatableField").animate({opacity: '0'}, 200).promise().done(function ()
			{
				//alert (ajaxUrl);
				//Do the ajax call
				$.ajax(
					{
						url: ajaxUrl,
						success: function(result)
						{
							//On success, process this data
							ProcessJSON(result);
							//Update page elements
							UpdatePageElements()
							//Show all hidden fields
							$(".UpdatableField").animate({opacity: '1'}, 200);
						} ,
						error: function( jqXHR, textStatus )
						{
							//Something rotten happened!!
							
							//Change all fields to # indicate an error and reshow them
							$(".UpdatableField").html("#");
							$(".UpdatableField").animate({opacity: '1'}, 200);
							
							//Display toast error
							ShowError("ERROR: Unable to complete AJAX call to server!", ToastTypes.ERROR);
							
						}
					}
				);
				
			}
		);
		
		

}



function LoadAlertData(alertType)
{
	var contentData = "Nothing";

	switch (alertType.toLowerCase())
	{
		case "warn":
			contentData = GenerateAlertHtml(DataCache.alerts.warnings, DataCache.alerts.counts.warnings, DataCache.alerts.dataFor);
			break;
		case "watch":
			contentData =  GenerateAlertHtml(DataCache.alerts.watches, DataCache.alerts.counts.watches, DataCache.alerts.dataFor);
			break;
		case "other":
			contentData =  GenerateAlertHtml(DataCache.alerts.statements, DataCache.alerts.counts.statements, DataCache.alerts.dataFor);
			break;

	}

	$("#alertPopup div").html( contentData );

}

function GenerateAlertHtml(inputObject, itemCount, dataFor)
{
	var output = "<ul class=''>";
	
	for (i=0; i<itemCount; i++)
	{
		var ci = inputObject[i];
		var dtString = moment(ci.date).format("ddd DD-MMM @ hh:MM A");
		var dispString = "";
		if (ci.disposition == "InEffect")
			dispString = "In effect for";
		else if (ci.disposition == "Ended")
			dispString = "Ended for";
		else
			dispString = "Unknown";
			
		var areasString = "";
		$.each(ci.areas, function(i)
		{
			areasString += "<li> &bull; " + ci.areas[i]	+ "</li>";
		});
		
		
		output += "<li>"; 
		output += "<h1>" + ci.caption + " [" + dataFor + "]</h1>";
		output += "<h2>Posted on: "  +  dtString + "</h2>";
		output += "<h2>" + dispString + ": <ul>" + areasString + "</ul></h2><br/>";
		output += "<h3>" + ci.contents + "</h3>";
		output += "</li>";
	}
	
	output += "</ul>";
	return output;
}



function SetRadarImages()
{
	var i;
	
	//Get number of items
	var len = Object.keys(Config.RadarSites).length
	
	for (i=0; i<len; i++)
	{
		//alert (RadarSources[i].Url);
		$("#RadarSelect").append("<option value='" + i.toString() + "'>" + Config.RadarSites[i].Caption + "</option>");
	}


    $("#RadarSelect").click(function() {
    	var sourceId = $("#RadarSelect option:selected").attr("value");
    	CurrentState.RadarSite = sourceId;
    	LoadRadarImage(sourceId);
    });
}

function SetSiteLists()
{
	var i;
	//Get number of items
	var len = Object.keys(Config.DataSites).length
	
	for (i=0; i<len; i++)
	{
		//alert (RadarSources[i].Url);
		$("#SiteSelect").append("<option value='" + i.toString() + "'>" + Config.DataSites[i].Caption + "</option>");
	}


    $("#SiteSelect").click(function() {
    	var sourceId = $("#SiteSelect option:selected").attr("value");
    	
    	LoadSiteData(sourceId)
    });
}

function LoadRadarImage(sourceId)
{
	
  
	var url = Config.RadarSites[sourceId].Url;

	//Replace placeholders with correct values
	url = url.replace("[w]", CurrentState.InitialPageWidth);
	url = url.replace("[h]", CurrentState.InitialPageHeight);
	
	$('#radarimg').attr("width", CurrentState.InitialPageWidth);
	$('#radarimg').attr("height", CurrentState.InitialPageHeight);
	$('#radarimg').attr("src", url);
	
	CurrentState.RadarSite = sourceId;
}

function LoadSiteData(sourceId)
{
	var url = "./inc/Ajax.GetData.py?type=conditions&for=" + sourceId.toString();
	UpdateSiteData(url);
	CurrentState.DataSite = sourceId;
}

function toCardinalDir(angleParam)
{
	//alert(angleParam);
	var angle = parseFloat(angleParam);
	//var ret = "";
	if ((angle >= 337.5) && (angle <= 360))
		return "N";
	else if ((angle >= 0) && (angle < 22.5))
		return "N";
	else if ((angle > 22.5) && (angle < 67.5))
		return "NE";
	else if ((angle >= 67.5) && (angle <= 112.5))
		return "E";
	else if ((angle > 112.5) && (angle < 157.5))
		return "SE";
	else if ((angle >= 157.5) && (angle <= 202.5))
		return "S";
	else if ((angle > 202.5) && (angle < 247.5))
		return "SW";
	else if ((angle >= 247.5) && (angle <= 292.5))
		return "W";
	else if ((angle > 292.5) && (angle < 337.5))
		return "NW";
	else
		return "#";
		
	
	
}


//Call when doc is done loading
$( document ).ready(function() {
	PreMain();
});



% Store the IoT channel ID and read API key
channelID = ;
readAPIKey = '';

% Provide the ThingSpeak alerts API key
alertApiKey = 'ECEGR_4640_01_LAB_01_THINGSPEAK_TEMPERATURE_API_KEY';

% Set the address for the HTTP call
alertUrl = "https://api.thingspeak.com/alerts/send";

% webwrite uses weboptions to add required headers. Alerts needs a ThingSpeak-Alerts-API-Key header.
options = weboptions("HeaderFields", ["ThingSpeak-Alerts-API-Key", alertApiKey]);

% Set the email subject
alertSubject = sprintf("Current Room Temperature");

% Read the most recent temperature data from Field 1
temp = thingSpeakRead(channelID, 'Fields', 1, 'ReadKey', readAPIKey);

% Check if data was read successfully
if isempty(temp)
    alertBody = "No data read from IoT device.";
else
    alertBody = sprintf("The current room temperature is %.2f.", temp);
end

% Try to send the alert
try
    webwrite(alertUrl, "body", alertBody, "subject", alertSubject, options);
catch someException
    fprintf("Failed to send alert: %s\n", someException.message);
end

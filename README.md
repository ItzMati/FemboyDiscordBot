# FemboyGuessingBot
A Discord bot that was supposed to have a game where you guess which image is the femboy but that doesnt work yet.

To make the /send_image command work you must add your own images folder. In that folder you should make folders from 1-however many you want. In the folders with numbers as titles you should put in the images. The bot will choose a random folder and then a random image from the folder. If you only have one folder named 1 then it will only chose from there.


It has 5 commands

## /send_image
This sends an image that i have

## /send_femboy {feed}
This sends a picture of a femboy from reddit. {feed} is the type of feed you want the image from (new, hot, top or rising)

## /random {high} {amount}
This sends {amount} random numbers from 0 to {high} 

#### Example
```
/random 100 3
```
```
59
79
10
```
## /send_number {number}
This sends the number you give it back to you

#### Example
```
/send_number 123
```
```
the number you said was 123
```
## /send_reddit {subreddit} {feed}
Sends an image from a subreddit. {feed} is the type of feed you want the image from (new, hot, top or rising)

## /help
This sends a message that describes each command. Kind of like this read me but shorter and less detailed.

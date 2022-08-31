## Hand Gesture Control | macOS

Hand gesture control made for macOS using OpenCV.
This is a project to develop my skill.
Anyone can use the code.


## FAQ

#### How are you changing the brightness on M1 macs?

I am using the Command-line display brightness control made by nriley. He used an brightness api which is available in macos but its undocumented. He did a great work of wrapping it as a pyobj with help of ctypes. I dont know the exact way how to do it but I just used the command line tool with the help of a subprocess.run()


#### How are you changing the volume?

I am just using the apple script and running it through terminal via subprocess.


## Acknowledgements

 - [A good insight on why this project is different than that on windows or linux](https://alexdelorenzo.dev/programming/2018/08/16/reverse_engineering_private_apple_apis.html)
 - [Terminal commands for brightness control](https://github.com/nriley/brightness)
 - [Different API for M1 Macs for controlling brightness (that arent even documented)](https://github.com/Hammerspoon/hammerspoon/issues/2668)
 - [Media Pipe](https://learnopencv.com/introduction-to-mediapipe/)

## Contributing

Contributions are always welcome!



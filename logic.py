from PyQt6.QtWidgets import *
from gui import *


class Logic:

    class Television(QMainWindow, Ui_TVRemote):

        MIN_VOLUME: int = 0
        MAX_VOLUME: int = 10
        MIN_CHANNEL: int = 1
        MAX_CHANNEL: int = 9


        def __init__(self) -> None:
            """
            A GUI-based television simulation that allows channel surfing, volume control,
            muting, and streaming via buttons and a slider interface.

            :return: None
            """
            super().__init__()
            self.setupUi(self)

            self.__status: bool = False
            self.__muted: bool = False
            self.__volume: int = self.MIN_VOLUME
            self.__channel: int = self.MIN_CHANNEL
            self.__prev_volume: int = self.MIN_VOLUME
            self.__other_channel_status: bool = False


            self.button_1.clicked.connect(lambda : self.set_channel(1))
            self.button_2.clicked.connect(lambda : self.set_channel(2))
            self.button_3.clicked.connect(lambda : self.set_channel(3))
            self.button_4.clicked.connect(lambda : self.set_channel(4))
            self.button_5.clicked.connect(lambda : self.set_channel(5))
            self.button_6.clicked.connect(lambda : self.set_channel(6))
            self.button_7.clicked.connect(lambda : self.set_channel(7))
            self.button_8.clicked.connect(lambda : self.set_channel(8))
            self.button_9.clicked.connect(lambda : self.set_channel(9))

            self.lcd_volume.display(self.__volume)

            self.button_mute.clicked.connect(self.mute)
            self.button_volume_up.clicked.connect(self.volume_up)
            self.button_volume_down.clicked.connect(self.volume_down)


            self.button_channel_up.clicked.connect(self.channel_up)
            self.button_channel_down.clicked.connect(self.channel_down)

            self.button_guide.clicked.connect(self.guide)
            self.button_exit.clicked.connect(self.exit)

            self.button_netflix.clicked.connect(lambda : self.set_streaming("Netflix"))
            self.button_hulu.clicked.connect(lambda : self.set_streaming("Hulu"))
            self.button_disney.clicked.connect(lambda : self.set_streaming("Disney+"))

            self.button_power.clicked.connect(self.power)

            self.slider_volume.valueChanged.connect(self.slider_volume_change)

            self.stackedWidget.setCurrentIndex(0)


        def mute(self) -> None:
            if self.__status:
                if not self.__muted:
                    self.__prev_volume = self.__volume
                    self.__volume = 0
                    self.slider_volume.setEnabled(False)
                else:
                    self.__volume = self.__prev_volume
                    self.slider_volume.setEnabled(True)
                self.__muted = not self.__muted

                self.lcd_volume.display(self.__volume)

        def slider_volume_change(self, slider: int) -> None:
            """
            Handles volume slider movement, updating internal volume value and display if TV is on and not muted.

            :param slider: The value from the slider.
            :return: None
             """
            if self.__status and not self.__muted:
                if slider != self.__volume:
                    self.__volume = slider
                    self.lcd_volume.display(self.__volume)


        def guide(self)-> None:
            """
            Displays the TV guide by switching the stacked widget to the guide index.

            :return: None
            """
            if self.__status:
                self.stackedWidget.setCurrentIndex(13)
                self.__other_channel_status = True


        def power(self) -> None:
            """
            Turns the television power on or off.
            :return: None
            """

            self.__status = not self.__status

            if self.__status:
                self.__channel = self.MIN_CHANNEL
                self.set_channel(self.__channel)

            else:
                self.stackedWidget.setCurrentIndex(0)


        def exit(self):
            """
            Exits the guide or streaming channels and returns to the last active channel.

            :return: None
            """
            if self.__status:
                self.__other_channel_status = False
                self.stackedWidget.setCurrentIndex(self.__channel)


        def channel_up(self) -> None:
            """
            Increases the channel number, wrapping around at MAX_CHANNEL.

            :return: None
            """
            if self.__status and self.__other_channel_status == False:
                if self.__channel ==self.MAX_CHANNEL:
                    self.__channel = self.MIN_CHANNEL
                else:
                    self.__channel += 1
                self.set_channel(self.__channel)


        def channel_down(self) -> None:
            """
            Decreases the channel by one. Wraps to MAX_CHANNEL if at MIN_CHANNEL.
            :return: None
            """
            if self.__status and self.__other_channel_status == False:
                if self.__channel == self.MIN_CHANNEL:
                    self.__channel = self.MAX_CHANNEL
                else:
                    self.__channel -= 1
                self.set_channel(self.__channel)


        def volume_up(self) -> None:
            """
            Increases volume by one tick, up to MAX_VOLUME. Unmutes TV if muted.

            :return: None
            """
            if self.__status:
                if self.__muted:
                    self.slider_volume.setEnabled(True)
                    self.__muted = False
                    self.__volume = self.__prev_volume
                    self.lcd_volume.display(self.__volume)
                    self.slider_volume.setValue(self.__volume)


                elif self.__volume < self.MAX_VOLUME and not self.__muted:
                    self.__volume += 1
                    self.__prev_volume = self.__volume
                    self.lcd_volume.display(self.__volume)
                    self.slider_volume.setValue(self.__volume)


        def volume_down(self) -> None:
            """
            Decreases the volume by one tick down to MIN_VOLUME.
            If muted, unmutes the TV and restores the previous volume before decreasing.
            :return: None
            """
            if self.__status:
                if self.__muted:
                    self.slider_volume.setEnabled(True)
                    self.__muted = False
                    self.__volume = self.__prev_volume
                    self.slider_volume.setValue(self.__volume)

                elif self.__volume > self.MIN_VOLUME:
                    self.__volume -= 1
                    self.__prev_volume = self.__volume
                    self.lcd_volume.display(self.__volume)
                    self.slider_volume.setValue(self.__volume)

        def set_channel(self, number: int) -> None:
            """
            Changes the channel to the specified number.

            :param number: The new channel number to switch to.
            :return: None
            """

            if self.__status and self.__other_channel_status == False:
                self.__channel = number
                print(self.__channel)

                # 1: "logos/ABC.png",
                # 2: "logos/NBC.png",
                # 3: "logos/ESPN.png",
                # 4: "logos/FOX.png",
                # 5: "logos/FoodNetwork.png",
                # 6: "logos/nickelodeon.png",
                # 7: "logos/HistoryChannels.png",
                # 8: "logos/CW.png",
                # 9: "logos/IonTelevision.png"

                #if self.MIN_CHANNEL <= self.__channel <= self;.MAX_CHANNEL:
                self.stackedWidget.setCurrentIndex(self.__channel)


        def set_streaming(self, service: str) -> None:
            """
            Changes the display to a streaming service screen.

            :param service: Name of the streaming service ("Netflix", "Hulu", or "Disney+").
            :return: None
            """
            if self.__status:
                if service == "Netflix":
                    self.stackedWidget.setCurrentIndex(10)
                    self.__other_channel_status = True
                elif service == "Hulu":
                    self.stackedWidget.setCurrentIndex(11)
                    self.__other_channel_status = True
                elif service == "Disney+":
                    self.stackedWidget.setCurrentIndex(12)
                    self.__other_channel_status = True



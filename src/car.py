

class Car:
    MAX_FUEL_LAPS = 100
    MAX_TIRE_LAPS = 100
    NUM_LAPS = 400

    def __init__(self):
        self.current_time = 0
        self.current_lap = 0
        self.fuel_tank = 18
        self.last_lap_fueled = 0
        self.last_lap_left_tires = 0
        self.last_lap_right_tires = 0
        self.is_caution = False
        self.racing = True

    def throw_caution(self):
        self.is_caution = True

    def get_lap_time(self):
        x = (0.5 * (self.current_lap - self.last_lap_left_tires)) + (0.5 * (self.current_lap - self.last_lap_right_tires))
        return 0.98 * (x ** 0.5) + 22.5

    def race_lap(self):
        self.current_time += self.get_lap_time()
        self.current_lap += 1

    def race_failed(self):
        fuel_out = (self.current_lap - self.last_lap_fueled) >= Car.MAX_FUEL_LAPS
        left_tires_out = (self.current_lap - self.last_lap_left_tires) >= Car.MAX_TIRE_LAPS
        right_tires_out = (self.current_lap - self.last_lap_right_tires) >= Car.MAX_TIRE_LAPS
        
        if fuel_out or left_tires_out or right_tires_out:
            self.racing = False
        return not self.racing

    def race_over(self):
        if self.current_lap >= Car.NUM_LAPS:
            self.racing = False
        return not self.racing

    def fuel_no_tires(self):
        x = self.current_lap - self.last_lap_fueled
        if not self.is_caution:
            self.current_time += 0.1 * x + 30
        else:
            self.current_time += 0.1 * x + 2
        
        self.fuel_tank = 18
        self.last_lap_fueled = self.current_lap
        self.current_lap += 1
    
    def change_left_tires(self):
        if not self.is_caution:
            self.current_time += 35
        else:
            self.current_time += 7

        self.last_lap_left_tires = self.current_lap
        self.current_lap += 1

    def change_right_tires(self):
        if not self.is_caution:
            self.current_time += 35
        else:
            self.current_time += 7

        self.last_lap_right_tires = self.current_lap
        self.current_lap += 1

    def change_four_tires(self):
        if not self.is_caution:
            self.current_time += 40
        else:
            self.current_time += 12

        self.last_lap_fueled = self.current_lap
        self.last_lap_left_tires = self.current_lap
        self.last_lap_right_tires = self.current_lap
        self.current_lap += 1

    def get_race_time(self):
        if self.current_time <= 60:
            return f"{round(self.current_time, 2)} seconds"
        minutes, seconds = divmod(self.current_time, 60)
        if minutes <= 60:
            return f"{int(minutes)} minutes and {round(seconds, 2)} seconds"
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)} hours, {int(minutes)} minutes, and {round(seconds, 2)} seconds"


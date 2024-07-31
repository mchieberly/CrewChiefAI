from src.car import Car

def race():
    car = Car()

    for lap in range(1, Car.NUM_LAPS + 1):
        
        need_fuel = (car.current_lap - car.last_lap_fueled) == 95
        need_left_tires = (car.current_lap - car.last_lap_left_tires) == 95
        need_right_tires = (car.current_lap - car.last_lap_right_tires) == 95

        if need_left_tires and need_right_tires:
            car.change_four_tires()
        elif need_left_tires:
            car.change_left_tires()
        elif need_right_tires:
            car.change_right_tires()
        elif need_fuel:
            car.fuel_no_tires()
        else:
            car.race_lap()

        if car.race_failed():
            print(f"Race failed on lap {lap}!")
            break
        if car.race_over():
            print(f"The race is over on lap {lap}!")
            break

        print(f"Lap {lap}: {format_time(car.get_lap_time())}")
        
    print(f"Total time: {format_time(car.current_time)}")


def format_time(seconds):
    if seconds <= 60:
        return f"{round(seconds, 2)} seconds"
    minutes, seconds = divmod(seconds, 60)
    if minutes <= 60:
        return f"{int(minutes)} minutes and {round(seconds, 2)} seconds"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)} hours, {int(minutes)} minutes, and {round(seconds, 2)} seconds"

race()


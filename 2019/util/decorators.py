from time import perf_counter


def timer(func):
    "Report time for decorated function to run."

    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        return_value = func(*args, **kwargs)
        durationMins = 0
        durationSecs = perf_counter() - start_time
        if durationSecs >= 60:
            durationMins = int(durationSecs/60)
            durationSecs -= durationMins * 60
        if durationMins > 0:
            print("This program ran in " + str(durationMins) + "minutes and "
                  + str(durationSecs) + " seconds.")
        else:
            print("This program ran in " + str(durationSecs) + " seconds.")
        return return_value

    return wrapper

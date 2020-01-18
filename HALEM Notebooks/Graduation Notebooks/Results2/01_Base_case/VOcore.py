import simpy
import datetime

import shapely
import shapely.geometry

import numpy as np
import pandas as pd
import openclsim.core as core
from scipy import interpolate

class GrainSize:
    """
    Add information on the grainsize to the object
    """

    def __init__(self, grain_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""
        self.grain_size = grain_size


class Pipeline:
    """
    Add information on the pipeline length to the object
    """

    def __init__(self, pipeline_lengths, volumes, nourishment_volume, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""

        pipeline_lengths.insert(0, pipeline_lengths[0])
        volumes.insert(0, 0)

        pipeline_lengths.append(pipeline_lengths[-1])
        volumes.append(volumes[-1] + 100000)

        # The total nourishment volume
        self.nourishment_volume = nourishment_volume

        # The interpolation function
        self.interpolate_function = interpolate.interp1d(volumes, pipeline_lengths, kind = "previous")
    
    def pipeline_length(self, volume):
        """
        Determine the length of the pipeline based on the sinker location and nourishmed volumes.
        """
        
        # Pumping duration
        return self.interpolate_function(volume) * 1
        

class TripCounter(core.HasContainer):
    """
    Create an event that increases the number of trips and calls event.succeed() once a number of trips is achieved.
    """

    def __init__(self, activity_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""

        self.activity_id = activity_id


class LoadingFunction:
    """
    Create a loading function and add it a processor.
    This is a generic and easy to read function, you can create your own LoadingFunction class and add this as a mixin.

    loading_rate: the rate at which units are loaded per second
    manoeuvring: the time it takes to manoeuvring in minutes
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""

    def loading(self, origin, destination, amount, add_trip = True):
        """
        Determine the duration of the loading event.
        This duration based is based on the pumped volume, pipeline length and grain size.
        """
        self.grain_size = origin.grain_size
        self.origin = origin

        counter = 1
        for msg in self.log["Message"]:
            if "unloading start" in msg:
                counter += 1

        technical_delay_dredging = 0

        if add_trip:
            self.trips[self.ActivityID].container.put(1)

            if origin.container.level - amount < self.min_filling / 100 * self.container.capacity:
                for _ in range(self.trips[self.ActivityID].container.capacity - self.trips[self.ActivityID].container.level):
                    self.trips[self.ActivityID].container.put(1)

            if self.delay:
                if counter == self.delay["Trip"] and "Dredging" == self.delay["When"]:
                    technical_delay_dredging = self.delay["Duration"]

                    self.log_entry(
                        "scheduled delay start",
                        self.env.now,
                        self.container.level,
                        self.geometry,
                        self.ActivityID,
                    )

                    self.log_entry(
                        "scheduled delay stop",
                        self.env.now + technical_delay_dredging,
                        self.container.level,
                        self.geometry,
                        self.ActivityID,
                    )
        
        if origin.name == "Area 212":
            return amount / (22_507 / 104) * 60 + technical_delay_dredging
        elif origin.name == "Area 228":
            return amount / (22_507 / 133) * 60 + technical_delay_dredging
        elif origin.name == "Area 494":
            return amount / (22_507 / 104) * 60 + technical_delay_dredging
        elif origin.name == "Area 511":
            return amount / (22_507 / 133) * 60 + technical_delay_dredging


class UnloadingFunction:
    """
    Create an unloading function and add it a processor.
    This is a generic and easy to read function, you can create your own LoadingFunction class and add this as a mixin.

    unloading_rate: the rate at which units are loaded per second
    manoeuvring: the time it takes to manoeuvring in minutes
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """Initialization"""

    def unloading(self, origin, destination, amount, add_trip = True):
        """
        Determine the duration of the unloading event.
        This duration based is based on the pumped volume, pipeline length and grain size.
        """

        counter = 1
        for msg in self.log["Message"]:
            if "unloading start" in msg:
                counter += 1

        technical_delay_pumping = 0

        if add_trip:
            if not hasattr(self, "previous_destination"):
                self.previous_destination = destination
            else:
                if destination != self.previous_destination:
                    additional_amount = self.previous_destination.container.level - self.previous_destination.nourishment_volume

                    if 0 < additional_amount:
                        self.previous_destination.container.reserve_get(additional_amount)
                        self.previous_destination.container.get(additional_amount)

                        destination.container.reserve_put(additional_amount)
                        destination.container.put(additional_amount)
                    
                    self.previous_destination = destination

            if destination.nourishment_volume < destination.container.level + amount:
                for _ in range(self.trips[self.ActivityID].container.capacity - self.trips[self.ActivityID].container.level):
                    self.trips[self.ActivityID].container.put(1)
            
            if (destination.container.capacity - destination.container.level - 5) < self.container.level:
                destination.container.get(5)

            if self.delay:
                if counter == self.delay["Trip"] and "Pumping" == self.delay["When"]:
                    technical_delay_pumping = self.delay["Duration"]

                    self.log_entry(
                        "scheduled delay start",
                        self.env.now,
                        self.container.level,
                        self.geometry,
                        self.ActivityID,
                    )

                    self.log_entry(
                        "scheduled delay stop",
                        self.env.now + technical_delay_pumping,
                        self.container.level,
                        self.geometry,
                        self.ActivityID,
                    )

        grain_size = origin.grain_size
        
        various_pipeline_lengths = [
            0,
            500,
            1000,
            1500,
            2000,
            2500,
            3000,
            3500,
            4000,
            4500,
            5000,
        ]
        
        # Area 212 and Area 494
        # Average grain size = 373 um
        if grain_size == 373:
            various_grainsizes = [
                214,
                209,
                204,
                200,
                194,
                176,
                157,
                132,
                111,
                80,
                59,
            ]
        
        # Area 228
        # Average grain size = 710 um
        elif grain_size == 710:
            various_grainsizes = [
                214,
                209,
                195,
                145,
                109,
                70,
                53,
                40,
                31,
                26,
                20,
            ]
        
        # Area 511
        # Average grain size = 533 um
        elif grain_size == 553:
            various_grainsizes = [
                214,
                209,
                204,
                186,
                144,
                114,
                85,
                61,
                47,
                38,
                29,
            ]
        
        interpolate_function = interpolate.interp1d(various_pipeline_lengths, various_grainsizes)
        
        # Pumping duration
        pumping_duration = 0
        destination_volume = destination.container.level
        
        # Calculate per 1_000 m3
        while destination_volume < destination.container.level + amount:

            pipeline_length = destination.pipeline_length(destination_volume) * 1
            pumping_duration += 1000 / interpolate_function(pipeline_length)

            destination_volume += 1000
        
        # (Dis)connecting duration
        dis_connecting = 20

        # Return seconds
        return (pumping_duration + dis_connecting) * 60 + technical_delay_pumping


class HasDepthRestriction:
    """HasDepthRestriction class

    Used to add depth limits to vessels
    draught: should be a lambda function with input variable container.volume
    waves: list with wave_heights
    ukc: list with ukc, corresponding to wave_heights

    filling: filling degree [%]
    min_filling: minimal filling degree [%]
    max_filling: max filling degree [%]
    """

    def __init__(
        self,
        compute_draught,
        ukc,
        waves=None,
        filling=None,
        min_filling=None,
        max_filling=None,
        step_size=1,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        """Initialization"""

        # Information required to determine whether vessel can access an area
        self.compute_draught = compute_draught
        self.ukc = ukc
        self.waves = waves

        # Information require to self-select filling degree
        if min_filling is not None and max_filling is not None:
            assert min_filling <= max_filling

        self.filling = int(filling) if filling is not None else None
        self.min_filling = int(min_filling) if min_filling is not None else int(0)
        self.max_filling = int(max_filling) if max_filling is not None else int(100)
        self.step_size = step_size

        if not self.filling:
            self.filling_degrees = np.linspace(
                self.min_filling,
                self.max_filling,
                (self.max_filling - self.min_filling) / self.step_size + 1,
                dtype=int,
            )
        else:
            self.fill_degrees = [self.filling]

        if not (max_filling - min_filling) % step_size == 0:
            raise ValueError("The difference between the minimum filling degree and maximum filling degree is not a multiple of the step size.")

        self.depth_data = {}
    
    def calc_water_depth(self, location, new_fill_degree = False):
        """
        Calculate the required waterdepth at the location for all times in the series
        """

        if not new_fill_degree:
            self.depth_data[location.name] = {}

            for i in self.filling_degrees:
                filling_degree = i / 100

                # Determine characteristics based on filling
                draught = self.compute_draught(filling_degree)

                # Make dataframe based on characteristics
                df = location.metocean_data.copy()
                df["Required depth"] = df[location.waveheight].apply(
                    lambda s: self.calc_required_depth(draught, s)
                )
            
                self.depth_data[location.name][i] = df
        
        else:

            # Determine characteristics based on filling
            draught = self.compute_draught(new_fill_degree / 100)

            # Make dataframe based on characteristics
            df = location.metocean_data.copy()
            df["Required depth"] = df[location.waveheight].apply(
                lambda s: self.calc_required_depth(draught, s)
            )
        
            self.depth_data[location.name][new_fill_degree] = df

    def check_optimal_filling(self, loader, unloader, origin, destination):
        """
        Check per varying filling degree:
         - waiting time
         - time back on site
         - volume transported
        """

        self.trip_selector = {
            "Filling Degree": [],
            "Volume": [],
            "Back on site": [],
            "Waiting": [],
            "Cycle production": [],
            "Trip production": [],
        }

        if destination.name not in self.depth_data.keys():
            self.calc_water_depth(destination)

        counter = 1
        for msg in self.log["Message"]:
            if "unloading start" in msg:
                counter += 1
    
        pumping_delay_duration = 0
        dredging_delay_duration = 0

        if self.delay:
            if counter == self.delay["Trip"]:
                if self.delay["When"] == "Dredging":
                    dredging_delay_duration = self.delay["Duration"]
                elif self.delay["When"] == "Pumping":
                    pumping_delay_duration = self.delay["Duration"]

        for i in self.filling_degrees:
            # Get date between now and 1 week ahead
            t_now = datetime.datetime.fromtimestamp(self.env.now - 3600)
            t_end = datetime.datetime.fromtimestamp(self.env.now + 7 * 24 * 3600)
            
            # Make dataframe based on characteristics
            df = self.depth_data[destination.name][i].copy()
            df = df[(df.index >= t_now) & (df.index <= t_end)]

            # Sailing distance
            distance = self.get_distance(origin.geometry, destination, verbose = False)[0]

            # Dredged amount
            amount = i / 100 * self.container.capacity

            # Determine the duration of each step
            duration_sailing_e = distance / self.compute_v(0)
            duration_sailing_f = distance / self.compute_v(i / 100)
            duration_dredging = self.loading(origin, destination, amount, add_trip = False)
            duration_pumping = self.unloading(self, destination, amount, add_trip = False)
            
            # Required window is the length of the pumping duration
            window_duration = duration_pumping

            # The arrival time
            arrival = self.env.now + duration_sailing_e + duration_dredging + duration_sailing_f + pumping_delay_duration + dredging_delay_duration

            # The cycle finish time
            finish = duration_sailing_e + duration_dredging + duration_sailing_f + duration_pumping + pumping_delay_duration + dredging_delay_duration
            
            # Check when the required depth <= water level 
            series = pd.Series(df["Required depth"] <= df[destination.waterdepth])

            # Determine waiting time
            waiting = self.determine_waiting_time(series, arrival, window_duration, self.compute_draught(i / 100))

            # Back on site
            back_on_site = finish + waiting

            # Save trip information
            self.trip_selector["Filling Degree"].append(int(i))
            self.trip_selector["Volume"].append(amount)
            self.trip_selector["Back on site"].append(back_on_site)
            self.trip_selector["Waiting"].append(waiting)
            self.trip_selector["Cycle production"].append(amount / finish)
            self.trip_selector["Trip production"].append(amount / back_on_site)
        
        df = pd.DataFrame.from_dict(self.trip_selector)
        optimal_volume = df[df["Trip production"] == max(df["Trip production"].values)]["Volume"]

        return optimal_volume[optimal_volume.index[0]]

    def determine_waiting_time(self, series, arrival, duration, draught):
        """
        Pandas script to check if there is a waiting event
        """

        # Reduce the duration because the depth requirement only is in the beginning
        duration = duration / 2

        # Loop through series to find windows
        index = series.index
        values = series.values
        in_range = False
        ranges = []
        for i, value in enumerate(values):
            if value == True:
                if i == 0:
                    begin = index[i]
                elif not in_range:
                    begin = index[i]

                in_range = True

            elif in_range:
                in_range = False
                end = index[i]

                if (end - begin) >= datetime.timedelta(seconds = duration):
                    ranges.append(
                        (begin.to_datetime64(), (end - datetime.timedelta(seconds = duration)).to_datetime64())
                    )
            
            if value == True and in_range == True and i + 1 == len(values):
                end = index[i]

                if (end - begin) >= datetime.timedelta(seconds = duration):
                    ranges.append(
                        (begin.to_datetime64(), (end - datetime.timedelta(seconds = duration)).to_datetime64())
                    )

        t = datetime.datetime.fromtimestamp(arrival)
        t = pd.Timestamp(t).to_datetime64()

        if ranges:
            i = np.array(ranges)[:, 0].searchsorted(t)
        else:
            # raise IndexError("No available water depth in the upcoming week, time is {} and draught is {}.".format(
            #     t, draught
            # ))
            return pd.Timedelta(index[-1] - t).total_seconds()

        if i > 0 and (np.array(ranges)[i - 1][0] <= t <= np.array(ranges)[i - 1][1]):
            return pd.Timedelta(0).total_seconds()
        elif i + 1 < len(ranges):
            return pd.Timedelta(np.array(ranges)[i, 0] - t).total_seconds()
        elif i + 1 == len(ranges):
            return pd.Timedelta(np.array(ranges)[i, 0] - t).total_seconds()
        else:
            raise IndexError("The tidal timeseries is exceeded!")
            

    def calc_depth_restrictions(self, location, fill_degree, duration):
        if location.name not in self.depth_data.keys():
            self.calc_water_depth(location)
        if fill_degree not in self.depth_data[location.name].keys():
            self.calc_water_depth(location, fill_degree)

        # Get date between now and 2 weeks ahead
        t_now = datetime.datetime.fromtimestamp(self.env.now - 3600)
        t_end = datetime.datetime.fromtimestamp(self.env.now + 3 * 24 * 3600)

        # Make dataframe based on characteristics
        df = self.depth_data[location.name][fill_degree].copy()
        df = df[(df.index >= t_now) & (df.index <= t_end)]
        series = pd.Series(df["Required depth"] <= df[location.waterdepth])

        # Determine waiting time
        waiting = self.determine_waiting_time(series, self.env.now, duration, self.compute_draught(fill_degree / 100))

        if waiting != 0:
            self.log_entry(
                "waiting for tide start",
                self.env.now,
                self.container.level,
                self.geometry,
                self.ActivityID,
            )
            yield self.env.timeout(waiting)
            self.log_entry(
                "waiting for tide stop",
                self.env.now,
                self.container.level,
                self.geometry,
                self.ActivityID,
            )

    def check_depth_restriction(self, location, fill_degree, duration):
        yield from self.calc_depth_restrictions(location, fill_degree * 100, duration)

    def calc_required_depth(self, draught, wave_height):
        required_depth = np.nan

        if self.waves:
            for i, wave in enumerate(self.waves):
                if wave_height <= wave:
                    required_depth = self.ukc[i] + draught

            return required_depth
        
        else:
            return self.ukc + draught

    @property
    def current_draught(self):
        return self.compute_draught(self.container.level / self.container.capacity)
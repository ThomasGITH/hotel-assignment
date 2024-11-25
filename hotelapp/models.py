from django.db import models


class City(models.Model):
    """
    City model. Contains a 'name' column as well as a 
    three-character 'code' column as a short form of 
    the name of the city.
    """

    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)

class Hotel(models.Model):
    """
    Hotel model. Contains a local_code, name of the hotel and
    the city that it's located it.

    Note that the 'local_code' is an identifier that's relative
     to the city that the hotel is in. So it is 'unique' among
     all the hotels in its city, but not unique amongst all the
     hotels in the database. The local_code is taken as the last
     two symbols of the center-column of the 'hotels' CSV data,
     e.g. 'A9' from 'BARA9'.

     The combination of 'local_code' and 'city' is used as
     a composite primary key, but the auto-generated 'id' column
     can be used as well.
    """

    local_code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    # Whether this should be 'PROTECT' or 'CASCADE' is debatable. I
    # think that 'PROTECT' makes more sense since, as long as hotels
    # exist, the city they're in ought to exist too.
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def global_code(self):
        """
        Returns the 'global code' i.e. the local code but with the
        city code behind it. This is the same formatting as in the
        CSV data.
        """

        return f"{self.city.code}{self.local_code}"

    class Meta:
        """
        Sets up a unique relationship between 'city' and 'local_code'.
        This enforces that in a city, there can be only one hotel with
        a specific code/number.
        """

        constraints = [
            models.UniqueConstraint(fields=['city', 'local_code'],
            name='unique_city_local_code')
        ]
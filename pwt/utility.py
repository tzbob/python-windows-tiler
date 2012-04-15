class Utility(object):

    @staticmethod
    def next_item(collection, item):
        """
        Returns the item after item
        Returns None if item isn't in collection
        """
        
        if item in collection:
        
            return collection[(collection.index(item) + 1) % len(collection)]
        
        return None

    @staticmethod
    def previous_item(collection, item):
        """
        Returns the item before item
        Returns None if item isn't in collection
        """

        if item in collection:

            return collection[collection.index(item) - 1]

        return None

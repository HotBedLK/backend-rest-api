import uuid



class GeneralUSerServiceUtils:
    """
    in this class we maintain all the general user service util functions.
    this class intantiated below of the page. so we can import that instance and use the functions of this class 
    """
    def IsValidModelId(self,expected_uuid:str)->bool:
        """
        Docstring for StringToUUID
        :param expected_uuid: expected string to convert to the uuid format
        :type expected_uuid: str
        :if expected_uuid is cannot to convert uuid that mean it is not uuid format. then we returen false. else we retun true
        """
        try:
            uuid.UUID(expected_uuid)
            return True
        except ValueError as e:
            print("expected uuid is not a type of uuid (cannot convert)",e)
            return False
        

utils = GeneralUSerServiceUtils()




from random import randint

class Address():
    '''IPv4 addresses'''
    def __init__(self, data):
        '''Создание интернет адреса'''
        assert(type(data) == int)
        self.data = data

    def __iter__(self):
        '''Перебор байтов интернет адреса'''
        for rank in [24, 16, 8, 0]:
            yield self.data >> rank & 0xff

    def __getitem__(self, key):
        assert(type(key) == int and 0 <= key <= 3)
        return self.data >> (8 * key) & 0xff

    def __int__(self):
        '''Представление интернет адреса в виде целого числа'''
        return self.data

    def __str__(self):
        '''Представление интернет адреса в виде строки'''
        return '.'.join(map(str, self))

class HostAddress(Address):
    '''Host addresses'''
    def __init__(self, address = None):
        '''Создание адреса компьютера.
        
        Если адрес не передаётся, он выбирается случайно в диапазоне [2**24; 2**32 - 2**24].'''
        if address is None:
            address = randint(2**24, 2**32 - 2**24)
        Address.__init__(self, address)

class NetworkMask(Address):
    '''Network mask'''
    def __init__(self, ones = None):
        '''Создание маски сети.
        
        В качестве необязательного параметра принимает количество единиц в маске. Если количество единиц не задаётся, оно выбирается случайно от 3 до 29 включительно.'''
        if ones is None:
            ones = randint(3, 29)
        self.ones = ones
        Address.__init__(self, (2**ones - 1) << (32 - ones))

    def ones(self):
        '''Возвращает количество единиц в маске сети.'''
        return self.ones

class NetworkAddress(Address):
    '''Network address'''
    def __init__(self, *args):
        '''Создание адреса сети.
        
        В качестве необязательных параметров принимает либо числовое значение сетевого адреса, либо адрес хоста и маску сети. Если параметры на передаются, то сетевой адрес выбирается случайно в диапазоне [2**24; 2**32 - 2**24].'''
        if len(args) == 0:
            Address.__init__(self, randint(2**24, 2**32 - 2**24))
        elif len(args) == 1:
            Address.__init__(self, args[0])
        elif len(args) == 2:
            Address.__init__(self, int(args[0]) & int(args[1]))

class TripleIPAddresses:
    '''«Сетевая тройка»: адрес компьютера, маска сети и адрес сети.'''
    def __init__(self):
        '''Создание «сетевой тройки».'''
        self._netmask_ = NetworkMask()
        self._host_ = HostAddress()
        self._network_ = NetworkAddress(self._host_, self._netmask_)

    def host(self):
        '''Возвращает адрес компьютера.'''
        return self._host_

    def netmask(self):
        '''Возвращает сетевую маску.'''
        return self._netmask_

    def network(self):
        '''Возвращает адрес сети.'''
        return self._network_

    def suitable(self):
        '''Возвращает список масок, которые подходят для данной пары хоста и сети.'''
        return [NetworkMask(m) for m in range(9) if int(NetworkAddress(self._host_, NetworkMask(m))) == int(self._network_)]

class TripleIPAddressesDeterminated(TripleIPAddresses):
    '''«Определённая» «сетевая тройка»: адрес компьютера, маска сети и адрес сети, в которой маску сети можно однозначно определить по адресам компьютера и сети.'''
    def __init__(self):
        '''Создание «определённой» «сетевой тройки».'''
        self._netmask_ = NetworkMask()
        self._host_ = HostAddress(int(HostAddress()) | 3 << (32 - 1 - self._netmask_.ones))
        self._network_ = NetworkAddress(self._host_, self._netmask_)

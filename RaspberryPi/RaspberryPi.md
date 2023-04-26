#### Obter o endereço MAC do dispositivo Bluetooth
```
$ hcitool dev | cut -sf3
```

### Ligar o ficheiro /dev/rfcomm0 ao endereço MAC
```
$ sudo rfcomm bind /dev/rfcomm0 <MAC>
```
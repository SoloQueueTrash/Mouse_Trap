class Trap {
  String name;
  String ip;
  int port;

  Trap({required this.name, required this.ip, required this.port});

  factory Trap.fromJson(Map<String, dynamic> json) {
    return Trap(
      name: json['name'],
      ip: json['ip'],
      port: json['port'],
    );
  }

  Map<String, dynamic> toJson() => {
        'name': name,
        'ip': ip,
        'port': port,
      };
}

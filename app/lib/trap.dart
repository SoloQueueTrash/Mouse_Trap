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

enum TrapStatus {
  open,
  closed,
  error,
  unknown,
}

extension TrapStatusExtension on TrapStatus {
  static TrapStatus fromString(String status) {
    switch (status) {
      case 'open':
        return TrapStatus.open;
      case 'closed':
        return TrapStatus.closed;
      case 'error':
        return TrapStatus.error;
      default:
        return TrapStatus.unknown;
    }
  }
}

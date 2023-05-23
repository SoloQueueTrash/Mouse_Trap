import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

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

  String get name {
    switch (this) {
      case TrapStatus.open:
        return 'Open';
      case TrapStatus.closed:
        return 'Closed';
      case TrapStatus.error:
        return 'Error';
      default:
        return 'Unknown';
    }
  }

  IconData get icon {
    switch (this) {
      case TrapStatus.open:
        return Icons.lock_open;
      case TrapStatus.closed:
        return Icons.lock;
      case TrapStatus.error:
        return Icons.error;
      default:
        return Icons.help;
    }
  }
}

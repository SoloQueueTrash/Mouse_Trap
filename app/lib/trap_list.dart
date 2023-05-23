import 'dart:convert';

import 'package:app/trap.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class TrapListScreen extends StatefulWidget {
  const TrapListScreen({Key? key}) : super(key: key);

  @override
  State<TrapListScreen> createState() => _TrapListScreenState();
}

class _TrapListScreenState extends State<TrapListScreen> {
  List<Trap> _traps = [];

  void _loadTraps() {
    SharedPreferences.getInstance().then((prefs) {
      var trapsJson = prefs.getStringList('traps');
      if (trapsJson == null) {
        return;
      }
      var traps = trapsJson.map((e) => Trap.fromJson(jsonDecode(e))).toList();
      setState(() => _traps = traps);
    });
  }

  void _saveTraps() {
    var trapsJson = _traps.map((e) => jsonEncode(e.toJson())).toList();
    SharedPreferences.getInstance().then((prefs) {
      prefs.setStringList('traps', trapsJson);
    });
  }

  @override
  void initState() {
    super.initState();
    _loadTraps();
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

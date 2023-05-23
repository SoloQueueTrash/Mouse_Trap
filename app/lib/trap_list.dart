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

  Widget _buildTrapItemContent(Trap trap, TrapStatus status) {
    var textColor = Theme.of(context).brightness == Brightness.light
        ? Colors.black
        : Colors.white;
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              trap.name,
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: textColor,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              '${trap.ip}:${trap.port}',
              style: TextStyle(fontSize: 14, color: textColor.withOpacity(0.7)),
            ),
          ],
        ),
        IconButton(
          icon: Icon(status.icon),
          color: status.color,
          onPressed: () {},
        )
      ],
    );
  }

  Widget _buildTrapItem(BuildContext context, int index) {
    var trap = _traps[index];
    return FutureBuilder(
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          } else {
            var status = snapshot.data as TrapStatus;
            return Container(
              margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              decoration: BoxDecoration(
                color: status.color.withOpacity(0.3),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: status.color, width: 2),
              ),
              child: _buildTrapItemContent(trap, status),
            );
          }
        },
        future: trap.getStatus());
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

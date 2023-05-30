import 'dart:convert';

import 'package:app/control_trap.dart';
import 'package:app/trap.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'add_trap.dart';

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
          enableFeedback:
              status == TrapStatus.open || status == TrapStatus.closed,
          icon: Icon(status.icon),
          color: status.color,
          onPressed: () {
            if (status == TrapStatus.open) {
              trap.close();
            } else if (status == TrapStatus.closed) {
              trap.open();
            }
            setState(() {});
          },
        )
      ],
    );
  }

  Widget _buildTrapItem(BuildContext context, int index) {
    var trap = _traps[index];
    return FutureBuilder(
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            var status = snapshot.data as TrapStatus;
            return GestureDetector(
                child: Container(
                  margin:
                      const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  padding:
                      const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  decoration: BoxDecoration(
                    color: status.color.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: status.color, width: 2),
                  ),
                  child: _buildTrapItemContent(trap, status),
                ),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => TrapControlScreen(trap: trap),
                    ),
                  ).then((_) {
                    setState(() {});
                  });
                });
          } else if (snapshot.hasError) {
            var status = TrapStatus.unknown;
            return GestureDetector(
                child: Container(
                  margin:
                      const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  padding:
                      const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                  decoration: BoxDecoration(
                    color: status.color.withOpacity(0.3),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: status.color, width: 2),
                  ),
                  child: _buildTrapItemContent(trap, status),
                ),
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Cannot connect to trap'),
                    ),
                  );
                });
          } else {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
        },
        future: trap.getStatus());
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton(
      onPressed: () {
        Navigator.push<Trap?>(
          context,
          MaterialPageRoute(
            builder: (context) => AddTrapScreen(),
          ),
        ).then((trap) {
          if (trap != null) {
            _addNewTrap(trap);
          }
        });
      },
      child: const Icon(Icons.add),
    );
  }

  void _addNewTrap(Trap trap) async {
    setState(() => _traps.add(trap));
    _saveTraps();
  }

  @override
  void initState() {
    super.initState();
    _loadTraps();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Traps'),
      ),
      body: RefreshIndicator(
        child: ListView.builder(
          itemBuilder: _buildTrapItem,
          itemCount: _traps.length,
        ),
        onRefresh: () async {
          setState(() {});
        },
      ),
      floatingActionButton: _buildFloatingActionButton(),
    );
  }
}

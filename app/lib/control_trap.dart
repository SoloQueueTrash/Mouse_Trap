import 'dart:typed_data';

import 'package:app/trap.dart';
import 'package:flutter/material.dart';

class TrapControlScreen extends StatefulWidget {
  final Trap trap;

  const TrapControlScreen({required this.trap});

  @override
  _TrapControlScreenState createState() => _TrapControlScreenState();
}

class _TrapControlScreenState extends State<TrapControlScreen> {
  Widget _buildTrapPicture() {
    return FutureBuilder(
      future: widget.trap.getPicture(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          var bytes = snapshot.data as Uint8List;
          return Image.memory(bytes);
        } else {
          return const CircularProgressIndicator();
        }
      },
    );
  }

  Widget _buildTrapStatus() {
    return FutureBuilder(
      future: widget.trap.getStatus(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          var status = snapshot.data as TrapStatus;
          return Text(
            status.name,
            style: TextStyle(
              color: status.color,
              fontSize: 24,
            ),
          );
        } else {
          return const CircularProgressIndicator();
        }
      },
    );
  }

  Widget _buildTrapControlButton() {
    return FutureBuilder(
      future: widget.trap.getStatus(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          var status = snapshot.data as TrapStatus;
          return ElevatedButton(
            onPressed: () {
              if (status == TrapStatus.open) {
                widget.trap.close();
              } else {
                widget.trap.open();
              }
              setState(() {});
            },
            child: Text(status == TrapStatus.open ? 'Close' : 'Open'),
          );
        } else {
          return const CircularProgressIndicator();
        }
      },
    );
  }

  Widget _buildTakePictureButton() {
    return ElevatedButton(
      onPressed: () {
        widget.trap.takePicture();
        setState(() {});
      },
      child: const Text('Picture'),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.trap.name),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _buildTrapPicture(),
            const SizedBox(height: 16),
            _buildTrapStatus(),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                _buildTrapControlButton(),
                const SizedBox(width: 16),
                _buildTakePictureButton(),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

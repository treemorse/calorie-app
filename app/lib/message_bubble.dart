import 'package:flutter/material.dart';

class MessageBubble extends StatelessWidget {
  final Alignment alignment;
  final Color color;
  final Color textColor;
  final Widget content;
  final Widget? leading;

  const MessageBubble({
    Key? key,
    required this.alignment,
    required this.color,
    required this.textColor,
    required this.content,
    this.leading,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      leading: leading,
      title: Align(
        alignment: alignment,
        child: Container(
          decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(12),
          ),
          padding: const EdgeInsets.all(10),
          child: DefaultTextStyle(
            style: TextStyle(color: textColor),
            child: content,
          ),
        ),
      ),
    );
  }
}

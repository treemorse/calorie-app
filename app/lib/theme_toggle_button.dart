import 'package:flutter/material.dart';

class ThemeToggleButton extends StatelessWidget {
  final VoidCallback toggleTheme;
  final bool isDarkTheme;

  const ThemeToggleButton({
    Key? key,
    required this.toggleTheme,
    required this.isDarkTheme,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: Icon(isDarkTheme ? Icons.light_mode : Icons.dark_mode),
      onPressed: toggleTheme,
    );
  }
}

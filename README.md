# Real time periodic task scheduling using Z3

This simple script is an attempt at finding real-time periodic
task schedules using Z3 SMT solver. Here is a small (harmonic)
task set schedule Z3 finds in less than a second:

![t_set_1](resources/t_set_1.png)

Here is a slightly more "problematic" schedule:

![t_set_2](resources/t_set_2.png)

More, slightly "bigger" task sets, still found in about a second:

![t_set_3](resources/t_set_3.png)

![t_set_4](resources/t_set_4.png)

![t_set_5](resources/t_set_5.png)

![t_set_6](resources/t_set_6.png)

Even bigger example found in 27 minutes (on AMD Ryzen 7 5700G):

![t_set_7](resources/t_set_7.png)

and in 7 minutes:

![t_set_8](resources/t_set_8.png)

The times needed for the bigger task sets might not seem impressive, but
finding a schedule in this setting is like searching in exponential space of size
2<sup>n_tasks &ast; hyper_period</sup>. In the last case it is 2<sup>3 &ast; 1386</sup>...


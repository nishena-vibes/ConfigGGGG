# Практика 1

### Задача 1

Вывести отсортированный в алфавитном порядке список имен пользователей в файле passwd (вам понадобится grep).

### Решение

```
reddy@CalmTurtle:~$ cat /etc/passwd | tr ":" " " | awk '{print $1}' | sort | head -n 10
_apt
backup
bin
daemon
dhcpcd
emilio
fwupd-refresh
games
iperf3
irc
```

### Задача 2

Вывести данные /etc/protocols в отформатированном и отсортированном порядке для 5 наибольших портов

### Решение

```
reddy@CalmTurtle:~$ cat /etc/protocols | grep -v '^[#|\s|\n]' | awk '{print $2, $1}' | sort -g -r | head -n 5
262 mptcp
143 ethernet
142 rohc
141 wesp
139 hip
```

### Задача 3

Написать программу banner средствами bash для вывода текстов, как в следующем примере (размер баннера должен меняться!):

```
[root@localhost ~]# ./banner "Hello from RTU MIREA!"
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
```

### Решение

```
#!/bin/bash

TOP_STR="+-"
MSG="$1"
for i in $(seq 2 "$(echo $MSG | wc -m)"); do
	TOP_STR="$TOP_STR-"
done

TOP_STR="$TOP_STR-+"

echo "$TOP_STR"
echo "| $MSG |"
echo "$TOP_STR"
```


### Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

### Решение

```
#!/bin/bash

chmod +x "$1"
cp "$1" /usr/local/bin       
```

### Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

### Решение
```
#!/bin/bash

files=(*.{c,js,py})

for file in "${files[@]}"; do
    read -r first_line < "$file" || continue

    case "${file##*.}" in
        c|js)
            regex='^[[:space:]]*(\/\/|\/\*)'
            ;;
        py)
            regex='^[[:space:]]*#'
            ;;
        *)
            continue
            ;;
    esac

    if [[ "$first_line" =~ $regex ]]; then
        echo "file '$file' contains comment: $first_line"
    fi
done
```


### Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

### Решение

```

```

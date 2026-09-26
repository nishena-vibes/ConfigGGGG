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

[Файл решения](banner.sh)

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

### Задача 4

Написать программу для вывода всех идентификаторов (по правилам C/C++ или Java) в файле (без повторений)

### Решение

[Файл решения](ident.sh)
```
#!/bin/bash

file="${1:?Укажи путь к файлу: $0 <file>}"

grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$file" \
  | tr '[:upper:]' '[:lower:]' \
  | sort -u \
  | tr '\n' ' ' \
  | sed 's/ $/\n/'
```


### Задача 5

Написать программу для регистрации пользовательской команды (правильные права доступа и копирование в /usr/local/bin).

### Решение

[Файл решения](reg)

```
#!/bin/bash

chmod +x "$1"
cp "$1" /usr/local/bin       
```

### Задача 6

Написать программу для проверки наличия комментария в первой строке файлов с расширением c, js и py.

### Решение

[Файл решения](6/cmtchk)

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

### Задача 7

Написать программу для нахождения файлов-дубликатов (имеющих 1 или более копий содержимого) по заданному пути (и подкаталогам).

### Решение

[Файл решения](7/dupes.sh)

```
#!/bin/bash

find $1 -type f -printf "%f\t%p\n" | sort | uniq -D -w $(find BRUHRR/ -type f -printf "%f\n" | wc -L)
```

### Задача 8

Написать программу, которая находит все файлы в данном каталоге с расширением, указанным в качестве аргумента и архивирует все эти файлы в архив tar.

### Решение

[Файл решения](8/arv)

```
#!/bin/bash

files=(*.$1)
archive_name="archive.tar"

echo ${files[@]}

if [ ${#files[@]} -eq 0 ]; then
	echo "No files to archive!";
	exit 1;
fi

if [ -n $2 ]; then
	archive_name=$2
fi

tar -cvf "$archive_name" "${files[@]}"
echo "Created archive $archive_name with files: $files"
```

### Задача 9

Написать программу, которая заменяет в файле последовательности из 4 пробелов на символ табуляции. Входной и выходной файлы задаются аргументами.

### Решение 

[Файл решения](4/sedrevamped)
```
#!/bin/bash

cat $1 | sed "s/    /\t/g" > $2
```

### Задача 10

Написать программу, которая выводит названия всех пустых текстовых файлов в указанной директории. Директория передается в программу параметром.

### Решение

[Файл решения](10/emptfls)
```
#!/bin/bash

dir=$1

ls -l "$dir" | awk '{print $5, $9}' | grep -E "0 .*\.txt" | awk '{print $2}'
```


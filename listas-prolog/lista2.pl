# Considere os fatos sobre professores, cursos e alunos

lectures(turing, 9020).
lectures(codd, 9311).
lectures(codd, 9314).

studies(fred, 9020).
studies(jack, 9311).
studies(jill, 9314).

year(fred, 1).
year(jack, 2).
year(jill, 2).


# Defina uma regra curso_assiste(Aluno, Professor) que é verdadeira se
# o Aluno estuda em algum curso que o Professor ensina.
curso_assiste(Aluno, Professor) :- studies(Aluno, Turma),
    							   lectures(Professor, Turma).

# Usando os operadores de comparação (como >, <, =:=, =\=), defina uma regra
# mais_avancado(S1, S2) que é verdadeira se o estudante S1 estiver em um ano
# estritamente maior que o estudante S2.
mais_avancado(S1, S2) :- year(S1, Y1), year(S2, Y2), Y1 > Y2.
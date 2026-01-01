# Defina o predicado soma_lista(Lista, SomaTotal) que unifica
# SomaTotal com a soma de todos os elementos da Lista.
soma_lista([], 0).
soma_lista([X | Y], SomaTotal) :- soma_lista(Y, SomaResto), SomaTotal is X + SomaResto.

# Defina o predicado classifica_nota(Nota, Conceito) que atribui um conceito
# com base na Nota. Use o operador Cut (!) para evitar que o Prolog
# procure outras soluções assim que uma faixa for satisfeita.
classifica_nota(Nota, 'excelente') :- Nota > 9, !.
classifica_nota(Nota, 'bom') :- Nota >= 6, !.
classifica_nota(_, 'insuficiente').

# Considere a seguinte base de conhecimento sobre estudantes:
aluno(101, joão, ia, 9.5).
aluno(102, ana, pcd, 7.0).
aluno(103, carlos, ia, 8.0).
aluno(104, bia, ia, 9.8).
aluno(105, pedro, bd, 5.5).

# Defina a regra melhor_aluno_ia(Nome) que encontra o Nome do aluno que
# obteve uma nota estritamente maior que 9.0 no curso 'ia' (Inteligência Artificial).
melhor_aluno_ia(Nome) :- aluno(_, Nome, ia, Nota), Nota > 9.0.

# Defina o predicado pertence_a_todos(Elemento, ListaDeListas)
# que é verdadeiro se o Elemento (member/2) estiver presente em todas as sublistas
# dentro da ListaDeListas.
pertence_a_todos(_, []).
pertence_a_todos(Elemento, [L1 | Resto]) :- member(Elemento, L1),
    										pertence_a_todos(Elemento, Resto).

# Considere a base de conhecimento de professores e disciplinas
# (predicado ensina(Professor, Disciplina))
ensina(turing, logica).
ensina(codd, bd).
ensina(codd, ia).
ensina(ferro, ia).ensina(turing, logica).
ensina(codd, bd).
ensina(codd, ia).
ensina(ferro, ia).

#  Defina uma regra ensina_ia_apenas(Professor) que é verdadeira se o Professor
# ensina apenas a disciplina 'ia'. (Use \+).
ensina_ia_apenas(Professor) :- ensina(Professor, ia), \+ (ensina(Professor, Outro), Outro \= ia).

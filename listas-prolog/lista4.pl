# Considere a seguinte base de fatos sobre uma árvore genealógica:

pai(ivo, eva).
pai(gil, rai).
pai(gil, clo).
pai(gil, ary).
pai(rai, noe).
pai(ary, gal).

mae(ana, eva).
mae(bia, rai).
mae(bia, clo).
mae(bia, ary).
mae(eva, noe).
mae(lia, gal).

# Acrescente ao programa os fatos necessários para definir as relações homem e mulher.
homem(ivo).
homem(gil).
homem(rai).
homem(ary).
homem(noe).

mulher(ana).
mulher(bia).
mulher(eva).
mulher(clo).
mulher(lia).
mulher(gal).

# Usando duas regras, defina a relação gerou(X,Y) tal que
# X gerou Y se X é pai ou mãe de Y.
gerou(X, Y) :- pai(X, Y); mae(X, Y).

# Usando relações já existentes, crie regras para definir as
# relações filho, filha, tio, tia, primo, prima, avô e avó.
filho(X, Y) :- homem(X), gerou(Y, X).

filha(X, Y) :- mulher(X), gerou(Y, X).

tio(X, Y) :- homem(X), gerou(Z, Y), pai(W, Z), pai(W, X), Z \= X.

tia(X, Y) :- mulher(X), gerou(Z, Y), pai(W, Z), pai(W, X), Z \= X.

primo(X, Y) :- homem(X), tio(Z, X), pai(Z, Y);
    homem(X), tia(Z, X), mae(Z, Y).

prima(X, Y) :- mulher(X), tio(Z, X), pai(Z, Y);
    mulher(X), tia(Z, X), mae(Z, Y).

avô(X, Y) :- pai(X, Z), gerou(Z, Y).

avó(X, Y) :- mae(X, Z), gerou(Z, Y).


# Codifique as regras equivalentes às seguintes sentenças:

# a) Todo mundo que tem filhos é feliz.
feliz(X) :- gerou(X, _).

# b) Um casal é formado por duas pessoas que têm filhos em comum.
casal(X, Y) :- gerou(X, Z), gerou(Y, Z), X \= Y.
# Considere a seguinte base de fatos e
# Crie as regras para definir a relação avô e irmão

pai(adão, caim).
pai(adão, abel).
pai(adão, seth).
pai(seth, enos).

avô(X, Y) :- pai(X, Z), pai(Z, Y).

irmão(X, Y) :- pai(Z, X), pai(Z, Y), X \= Y.


# Qual consulta deve ser feita para encontrar as seguintes informações?

# Quem é pai de Adão?
pai(X, adão)
 
# Quem são os filhos de Adão?
pai(adão, X)
 
# Quem são os netos de Adão?
avô(adão, X)
 
# Quem são os tios de Enos? Y
pai(X, enos), irmao(Y, X)
 
# Quem é o avô de Enos?
avô(X, enos)

# Quem são os irmãos de Caim?
irmão(X, caim)
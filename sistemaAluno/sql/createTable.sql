use db_escola;

create view vw_notas_alunos as

select a.aluno_id, b.nome_aluno, a.disciplina_id, a.nota, c.nome_disciplina
from tb_notas as a 
inner join tb_alunos as b
on a.aluno_id=b.id
inner join tb_disciplinas as c
on a.disciplina_id = c.id

select * from vw_notas_alunos


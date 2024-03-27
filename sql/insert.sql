-- Insert into role
INSERT INTO role (name) VALUES ('Solucionador');
INSERT INTO role (name) VALUES ('Solicitante');

-- Insert into state
INSERT INTO state (name) VALUES ('Nuevo');
INSERT INTO state (name) VALUES ('Aprobado');
INSERT INTO state (name) VALUES ('Solucionando');
INSERT INTO state (name) VALUES ('Solucionado');
INSERT INTO state (name) VALUES ('Cerrado');
INSERT INTO state (name) VALUES ('Cancelado');

-- Insert into position
INSERT INTO position (name) VALUES ('Analista');
INSERT INTO position (name) VALUES ('Estudiante');
INSERT INTO position (name) VALUES ('Docente');
INSERT INTO position (name) VALUES ('Personal de seguridad');
INSERT INTO position (name) VALUES ('Personal de aseo');
INSERT INTO position (name) VALUES ('Vendedor');

-- Insert into department
INSERT INTO department (name, active_members) VALUES ('Administración', 20);
INSERT INTO department (name, active_members) VALUES ('Operaciones', 20);
INSERT INTO department (name, active_members) VALUES ('Decanatura', 20);
INSERT INTO department (name, active_members) VALUES ('Ninguno', 0);

-- Insert into category
INSERT INTO category (name) VALUES ('Dudas catedra');
INSERT INTO category (name) VALUES ('Dudas operacionales');
INSERT INTO category (name) VALUES ('Dudas administrativas');
INSERT INTO category (name) VALUES ('Dudas procedimentales');
INSERT INTO category (name) VALUES ('Reclamos catedra');
INSERT INTO category (name) VALUES ('Reclamos operacionales');
INSERT INTO category (name) VALUES ('Reclamos administrativas');
INSERT INTO category (name) VALUES ('Reclamos procedimentales');
INSERT INTO category (name) VALUES ('Solicitudes catedra');
INSERT INTO category (name) VALUES ('Solicitudes operacionales');
INSERT INTO category (name) VALUES ('Solicitudes administrativas');
INSERT INTO category (name) VALUES ('Solicitudes procedimentales');

-- Insert into person
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('John Doe', '12345', 'john@example.com', 2, 2, 4);
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('Jane Doe', '12346', 'jane@example.com', 3, 2, 3);
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('Alex Doe', '12347', 'alex@example.com', 3, 1, 1);
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('Miranda Doe', '12348', 'miranda@example.com', 4, 2, 2);
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('William Doe', '12349', 'william@example.com', 5, 1, 1);
INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES ('Solver Doe', '12355', 'solver@example.com', 1, 1, 1);


-- Insert into request
INSERT INTO request (generated_at, summary, category_id, solver_id, requester_id, state_id) VALUES ('2024-03-02', 'General request', 3, 6, 1, 1);
INSERT INTO request (generated_at, summary, category_id, solver_id, requester_id, state_id) VALUES ('2024-03-02', 'Class request', 9, NULL, 2, 1);

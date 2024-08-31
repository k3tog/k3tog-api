\connect k3tog_dev_db;

ALTER TABLE IF EXISTS k3tog."user"
    ADD CONSTRAINT fk_user_preferred_language_id FOREIGN KEY (preferred_language_id)
    REFERENCES k3tog."language" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."project"
    ADD CONSTRAINT fk_project_user_id FOREIGN KEY (user_id)
    REFERENCES k3tog."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."project"
    ADD CONSTRAINT fk_project_pattern_id FOREIGN KEY (pattern_id)
    REFERENCES k3tog."user_pattern" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."user_gauge"
    ADD CONSTRAINT fk_user_gauge_user_id FOREIGN KEY (user_id)
    REFERENCES k3tog."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."user_gauge"
    ADD CONSTRAINT fk_user_gauge_yarn_id FOREIGN KEY (yarn_id)
    REFERENCES k3tog."user_yarn" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."user_gauge"
    ADD CONSTRAINT fk_user_gauge_needle_id FOREIGN KEY (needle_id)
    REFERENCES k3tog."user_needle" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."user_needle"
    ADD CONSTRAINT fk_user_needle_user_id FOREIGN KEY (user_id)
    REFERENCES k3tog."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."user_pattern"
    ADD CONSTRAINT fk_user_pattern_user_id FOREIGN KEY (user_id)
    REFERENCES k3tog."user" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."user_yarn"
    ADD CONSTRAINT fk_user_yarn_user_id FOREIGN KEY (user_id)
    REFERENCES k3tog."user" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."project_needle"
    ADD CONSTRAINT fpk_project_needle_project_id FOREIGN KEY (project_id)
    REFERENCES k3tog."project" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."project_needle"
    ADD CONSTRAINT fpk_project_needle_needle_id FOREIGN KEY (needle_id)
    REFERENCES k3tog."user_needle" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."project_yarn"
    ADD CONSTRAINT fpk_project_yarn_project_id FOREIGN KEY (project_id)
    REFERENCES k3tog."project" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."project_yarn"
    ADD CONSTRAINT fpk_project_yarn_yarn_id FOREIGN KEY (yarn_id)
    REFERENCES k3tog."user_yarn" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."project_gauge"
    ADD CONSTRAINT fpk_project_gauge_project_id FOREIGN KEY (project_id)
    REFERENCES k3tog."project" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS k3tog."project_gauge"
    ADD CONSTRAINT fpk_project_gauge_gauge_id FOREIGN KEY (gauge_id)
    REFERENCES k3tog."user_gauge" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."pattern_document"
    ADD CONSTRAINT fpk_pattern_document_pattern_id FOREIGN KEY (pattern_id)
    REFERENCES k3tog."user_pattern" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL;

ALTER TABLE IF EXISTS k3tog."photo"
    ADD CONSTRAINT fpk_user_yarn_photo FOREIGN KEY (reference_id)
    REFERENCES k3tog."user_yarn" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."photo"
    ADD CONSTRAINT fpk_user_needle_photo FOREIGN KEY (reference_id)
    REFERENCES k3tog."user_needle" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."photo"
    ADD CONSTRAINT fpk_project_photo FOREIGN KEY (reference_id)
    REFERENCES k3tog."project" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;

ALTER TABLE IF EXISTS k3tog."photo"
    ADD CONSTRAINT fpk_user_gauge_photo FOREIGN KEY (reference_id)
    REFERENCES k3tog."user_gauge" (id) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE SET NULL
    NOT VALID;

-- ALTER TABLE IF EXISTS k3tog."photo"
--     ADD CONSTRAINT photo_type_check CHECK (
--         (type = 'user_yarn' AND reference_id IN (SELECT id FROM k3tog."user_yarn")) OR
--         (type = 'user_needle' AND reference_id IN (SELECT id FROM k3tog."user_needle")) OR
--         (type = 'project' AND reference_id IN (SELECT id FROM k3tog."project")) OR
--         (type = 'user_gauge' AND reference_id IN (SELECT id FROM k3tog."user_gauge"))
--     );

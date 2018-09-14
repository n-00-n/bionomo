CREATE TABLE bionomo_pilot_dev.multimedia
(
    id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    description varchar(100),
    type int(11),
    `order` int(11),
    collection_id int(11),
    provider_id int(11),
    full_name varchar(50),
    short_name varchar(50),
    provider_abbrv varchar(10),
    CONSTRAINT multimedia_ibfk_1 FOREIGN KEY (collection_id) REFERENCES collection (id),
    CONSTRAINT multimedia_ibfk_2 FOREIGN KEY (provider_id) REFERENCES provider (id)
);
CREATE INDEX collection_id ON bionomo_pilot_dev.multimedia (collection_id);
CREATE INDEX ix_multimedia_type ON bionomo_pilot_dev.multimedia (type);
CREATE INDEX provider_id ON bionomo_pilot_dev.multimedia (provider_id);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Eduardo Mondlane University', 4, null, null, null, 'logo-uem.png', 'logo_uem', 'UEM');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Univeristy Sapienzia', 4, null, null, null, 'logo-unisapienzia.png', 'logo_unisapienzia', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Natural History Museum of Maputo', 4, null, null, null, 'logo-museu.png', 'logo_museu', 'MHN');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Instituto Nacional de Investigacao Agraria', 4, null, null, null, 'logo-iiam.png', 'logo_iiam', 'IIAM');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Agenzia Italiana', 4, null, null, null, 'logo-aics.png', 'logo_aics', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of BioNoMo - Biodiversity Network of Mozambique', 4, null, null, null, 'logo-bionomo.png', 'logo_bionomo', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('thumbnail of Natural History Museum of Maputo', 1, null, null, null, 'thumb-museu.jpg', 'thumb_museu', 'MHN');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('flag of Portugal', 5, null, null, null, 'flag_pt-24.png', 'flag_pt', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('flag of United Kingdom', 5, null, null, null, 'flag_uk-24.png', 'flag_uk', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('flag of Italy', 5, null, null, null, 'flag_it-24.png', 'flag_it', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('flag of France', 5, null, null, null, 'flag_fr-24.png', 'flag_fr', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of MITADER', 4, null, null, null, 'logo-mitader.png', 'logo_mitader', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('thumbnail of MITADER', 1, null, null, null, 'thumb-mitader.jpg', 'thumb_mitader', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of the Department of Biological Sciences', 4, null, null, null, 'logo-dcb.png', 'logo_dcb', null);
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Instituto de Investigação Pesqueira', 4, null, null, null, 'logo-iip.png', 'logo_iip', 'IIP');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('thumbnail of Insituto de Investigação Pesqueira', 1, null, null, null, 'thumb-iip.jpg', 'thumb_iip', 'IIP');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Mozambique National Forest Inventory', 4, null, null, null, 'logo-dinaf.png', 'logo_dinaf', 'DINAF');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('thumbnail of Mozambique National Forest Inventory', 1, null, null, null, 'thumb-dinaf.jpg', 'thumb_dinaf', 'DINAF');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('logo of Centro de BioTecnologia', 4, null, null, null, 'logo-cb.png', 'logo_cb', 'CB');
INSERT INTO bionomo_pilot_dev.multimedia (description, type, `order`, collection_id, provider_id, full_name, short_name, provider_abbrv) VALUES ('thumbnail of Instituto Nacional de Investigacao Agraria', 1, null, null, null, 'thumb-iiam.jpg', 'thumb_iiam', 'IIAM');
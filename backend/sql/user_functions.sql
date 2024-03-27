create function get_request_id() returns INTEGER DETERMINISTIC NO SQL return @request_id;

create function get_person_id() returns INTEGER DETERMINISTIC NO SQL return @person_id;
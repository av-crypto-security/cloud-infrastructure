-- =====================================================
-- Schema: Industrial Monitoring System
-- =====================================================

CREATE SCHEMA IF NOT EXISTS app;
SET search_path TO app;

-- =====================================================
-- Employees
-- =====================================================

CREATE TABLE app.employee (
    employee_id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    position TEXT NOT NULL,
    qualification TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================
-- Qualification Checks
-- =====================================================

CREATE TABLE app.qualification_check (
    check_id BIGSERIAL PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    check_date DATE NOT NULL,
    result TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_qualification_employee
        FOREIGN KEY (employee_id)
        REFERENCES app.employee(employee_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_qualification_employee
    ON app.qualification_check(employee_id);

-- =====================================================
-- Facilities
-- =====================================================

CREATE TABLE app.facility (
    facility_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    facility_type TEXT NOT NULL,
    location TEXT,
    construction_date DATE,
    condition TEXT CHECK (condition IN ('GOOD','WARNING','CRITICAL')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================
-- Equipment
-- =====================================================

CREATE TABLE app.equipment (
    equipment_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    facility_id BIGINT NOT NULL,
    installed_at DATE,
    condition TEXT CHECK (condition IN ('OPERATIONAL','MAINTENANCE','FAILED')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_equipment_facility
        FOREIGN KEY (facility_id)
        REFERENCES app.facility(facility_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_equipment_facility
    ON app.equipment(facility_id);

-- =====================================================
-- Monitoring Parameters
-- =====================================================

CREATE TABLE app.monitoring_parameter (
    parameter_id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    unit_of_measure TEXT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- =====================================================
-- Monitoring Records
-- =====================================================

CREATE TABLE app.monitoring_record (
    record_id BIGSERIAL PRIMARY KEY,
    parameter_id BIGINT NOT NULL,
    equipment_id BIGINT NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_monitoring_parameter
        FOREIGN KEY (parameter_id)
        REFERENCES app.monitoring_parameter(parameter_id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_monitoring_equipment
        FOREIGN KEY (equipment_id)
        REFERENCES app.equipment(equipment_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_monitoring_equipment_time
    ON app.monitoring_record(equipment_id, recorded_at DESC);

CREATE INDEX idx_monitoring_parameter
    ON app.monitoring_record(parameter_id);

-- =====================================================
-- Inspections
-- =====================================================

CREATE TABLE app.inspection (
    inspection_id BIGSERIAL PRIMARY KEY,
    facility_id BIGINT NOT NULL,
    inspection_date DATE NOT NULL,
    result TEXT NOT NULL,
    recommendations TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT fk_inspection_facility
        FOREIGN KEY (facility_id)
        REFERENCES app.facility(facility_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_inspection_facility
    ON app.inspection(facility_id);

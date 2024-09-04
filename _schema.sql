--
-- PostgreSQL database dump
--

-- Dumped from database version 15.8
-- Dumped by pg_dump version 16.0

-- Started on 2024-09-03 19:21:17 EDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 32768)
-- Name: taxis; Type: TABLE; Schema: public; Owner: default
--

CREATE TABLE public.taxis (
    id integer NOT NULL,
    plate character varying(255)
);


ALTER TABLE public.taxis OWNER TO "default";

--
-- TOC entry 216 (class 1259 OID 32774)
-- Name: trajectories; Type: TABLE; Schema: public; Owner: default
--

CREATE TABLE public.trajectories (
    id integer NOT NULL,
    taxi_id integer NOT NULL,
    date timestamp without time zone,
    latitude double precision,
    longitude double precision
);


ALTER TABLE public.trajectories OWNER TO "default";

--
-- TOC entry 215 (class 1259 OID 32773)
-- Name: trajectories_id_seq; Type: SEQUENCE; Schema: public; Owner: default
--

CREATE SEQUENCE public.trajectories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trajectories_id_seq OWNER TO "default";

--
-- TOC entry 2555 (class 0 OID 0)
-- Dependencies: 215
-- Name: trajectories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: default
--

ALTER SEQUENCE public.trajectories_id_seq OWNED BY public.trajectories.id;


--
-- TOC entry 217 (class 1259 OID 65536)
-- Name: users; Type: TABLE; Schema: public; Owner: default
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.user_id_seq'::regclass) NOT NULL,
    email character varying(50) NOT NULL,
    name character varying(100),
    password character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO "default";

--
-- TOC entry 2399 (class 2604 OID 32777)
-- Name: trajectories id; Type: DEFAULT; Schema: public; Owner: default
--

ALTER TABLE ONLY public.trajectories ALTER COLUMN id SET DEFAULT nextval('public.trajectories_id_seq'::regclass);


--
-- TOC entry 2402 (class 2606 OID 32772)
-- Name: taxis taxis_pkey; Type: CONSTRAINT; Schema: public; Owner: default
--

ALTER TABLE ONLY public.taxis
    ADD CONSTRAINT taxis_pkey PRIMARY KEY (id);


--
-- TOC entry 2404 (class 2606 OID 32779)
-- Name: trajectories trajectories_pkey; Type: CONSTRAINT; Schema: public; Owner: default
--

ALTER TABLE ONLY public.trajectories
    ADD CONSTRAINT trajectories_pkey PRIMARY KEY (id);


--
-- TOC entry 2406 (class 2606 OID 65540)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: default
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2407 (class 2606 OID 32780)
-- Name: trajectories trajectories_taxi_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: default
--

ALTER TABLE ONLY public.trajectories
    ADD CONSTRAINT trajectories_taxi_id_fkey FOREIGN KEY (taxi_id) REFERENCES public.taxis(id);


-- Completed on 2024-09-03 19:21:24 EDT

--
-- PostgreSQL database dump complete
--


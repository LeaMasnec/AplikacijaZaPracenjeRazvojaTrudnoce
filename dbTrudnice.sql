PGDMP                         z            trudnoca    14.1    14.1 5    3           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            4           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            5           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            6           1262    16394    trudnoca    DATABASE     g   CREATE DATABASE trudnoca WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Croatian_Croatia.1252';
    DROP DATABASE trudnoca;
                postgres    false            ?            1255    16558 "   azuriraj_tablicu(integer, integer)    FUNCTION     ?  CREATE FUNCTION public.azuriraj_tablicu(korisnik integer, brojtjedna integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare 
trenutniTjedan int;
begin
select "Broj tjedna" into trenutniTjedan from "Tjedan trudnoce" where korisnickiracunid=korisnik;
if brojTjedna>trenutniTjedan then
UPDATE "Tjedan trudnoce"
SET "Broj tjedna" = brojTjedna 
WHERE korisnickiracunid = korisnik;
end if;
end; $$;
 M   DROP FUNCTION public.azuriraj_tablicu(korisnik integer, brojtjedna integer);
       public          postgres    false            ?            1255    16586    datum_rodenja(date)    FUNCTION     ?   CREATE FUNCTION public.datum_rodenja(datumzaceca date) RETURNS date
    LANGUAGE plpgsql
    AS $$
declare
datumRodenja date;
begin
select datumZaceca + interval '9 month' into datumRodenja;
return datumRodenja;
end; $$;
 6   DROP FUNCTION public.datum_rodenja(datumzaceca date);
       public          postgres    false            ?            1255    16750 
   dodajlog()    FUNCTION     ?   CREATE FUNCTION public.dodajlog() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
	
BEGIN
	INSERT INTO public.login_log(
	idlog, korisnickiracunid, datum_logina)
	VALUES (default, new."idKorisnicki racun", CURRENT_TIMESTAMP);
	return new;
END;$$;
 !   DROP FUNCTION public.dodajlog();
       public          postgres    false            ?            1255    16642    dodajpraznebiljeske()    FUNCTION     ?  CREATE FUNCTION public.dodajpraznebiljeske() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
INSERT INTO biljeska(
"idBiljeska", mjesec, "KorisnickiRacunID", zadnji_update, biljeska)
VALUES (default, 0, new."idKorisnicki racun", null, null),
(default, 1, new."idKorisnicki racun", null, null),
(default, 2, new."idKorisnicki racun", null, null),
(default, 3, new."idKorisnicki racun", null, null),
(default, 4, new."idKorisnicki racun", null, null),
(default, 5, new."idKorisnicki racun", null, null),
(default, 6, new."idKorisnicki racun", null, null),
(default, 7, new."idKorisnicki racun", null, null),
(default, 8, new."idKorisnicki racun", null, null),
    (default, 9, new."idKorisnicki racun", null, null);
return new;
END;$$;
 ,   DROP FUNCTION public.dodajpraznebiljeske();
       public          postgres    false            ?            1255    16555    dohvati_ime_korisnice(integer)    FUNCTION       CREATE FUNCTION public.dohvati_ime_korisnice(korisnik integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare 
naziv varchar(100);
begin
select "ime" || ' ' || "prezime" into naziv from "Korisnicki Racun" 
where "idKorisnicki racun"=korisnik;
return naziv;
end; $$;
 >   DROP FUNCTION public.dohvati_ime_korisnice(korisnik integer);
       public          postgres    false            ?            1255    16552 5   login_korisnika(character varying, character varying)    FUNCTION     ?  CREATE FUNCTION public.login_korisnika(korime character varying, pass character varying) RETURNS TABLE("idUser" integer, username character varying, password character varying, "CreationDate" date, "LastLogin" timestamp without time zone)
    LANGUAGE plpgsql
    AS $$
begin
return query select
"idKorisnicki racun", "korisnicko ime", "lozinka", "datum kreiranja racuna", "zadnja prijava"
from "Korisnicki Racun" where "korisnicko ime"=korime AND lozinka=pass;
end; $$;
 X   DROP FUNCTION public.login_korisnika(korime character varying, pass character varying);
       public          postgres    false            ?            1255    16600    prosli_mjeseci(integer)    FUNCTION     ?  CREATE FUNCTION public.prosli_mjeseci(korisnik integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
declare 
protekliMjeseci int;
datumZaceca date;
begin
select datum_zaceca into datumZaceca from "Tjedan trudnoce" where korisnickiracunid=korisnik;
SELECT (DATE_PART('year', CURRENT_TIMESTAMP::date) - DATE_PART('year', datumZaceca::date)) * 12 +
              (DATE_PART('month', CURRENT_TIMESTAMP::date) - DATE_PART('month', datumZaceca::date)) into protekliMjeseci;
return protekliMjeseci;
end; $$;
 7   DROP FUNCTION public.prosli_mjeseci(korisnik integer);
       public          postgres    false            ?            1255    16556    prosli_tjedni(integer)    FUNCTION     ?  CREATE FUNCTION public.prosli_tjedni(korisnik integer) RETURNS integer
    LANGUAGE plpgsql
    AS $$
declare 
protekliTjedni int;
datumZaceca date;
begin
select datum_zaceca into datumZaceca from "Tjedan trudnoce" where korisnickiracunid=korisnik;
SELECT TRUNC(DATE_PART('day', CURRENT_TIMESTAMP::timestamp - datumZaceca::timestamp)/7) into protekliTjedni;
return protekliTjedni;
end; $$;
 6   DROP FUNCTION public.prosli_tjedni(korisnik integer);
       public          postgres    false            ?            1255    16735    provjerimjesec()    FUNCTION     m  CREATE FUNCTION public.provjerimjesec() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare 
	protekliMjeseci int;
	datumZaceca date;
BEGIN
	select datum_zaceca into datumZaceca from "Tjedan trudnoce" where NEW."KorisnickiRacunID"="Tjedan trudnoce".korisnickiracunid;
	SELECT (DATE_PART('year', CURRENT_TIMESTAMP::date) - DATE_PART('year', datumZaceca::date)) * 12 +
              (DATE_PART('month', CURRENT_TIMESTAMP::date) - DATE_PART('month', datumZaceca::date)) into protekliMjeseci;
	if new.mjesec>protekliMjeseci THEN
		RAISE EXCEPTION 'Niste jos u tom mjesecu trudnoce!';
	ELSE
	return new;
	end if;
	
END;$$;
 '   DROP FUNCTION public.provjerimjesec();
       public          postgres    false            ?            1255    16567    trigger_azurirajbrojtjedna()    FUNCTION     ?  CREATE FUNCTION public.trigger_azurirajbrojtjedna() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare 
protekliTjedni int;
BEGIN
SELECT TRUNC(DATE_PART('day', CURRENT_TIMESTAMP::timestamp - NEW.datum_zaceca::timestamp)/7) into protekliTjedni;
    IF NEW."Broj tjedna" IS NULL THEN
        Update "Tjedan trudnoce"
set "Broj tjedna"=protekliTjedni
where idtjedantrudnoce=new.idtjedantrudnoce;
    END IF;
return new;
END;$$;
 3   DROP FUNCTION public.trigger_azurirajbrojtjedna();
       public          postgres    false            ?            1255    16594 "   trigger_azurirajbrojtjednaupdate()    FUNCTION     ?  CREATE FUNCTION public.trigger_azurirajbrojtjednaupdate() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
declare 
protekliTjedni int;
BEGIN
SELECT TRUNC(DATE_PART('day', CURRENT_TIMESTAMP::timestamp - NEW.datum_zaceca::timestamp)/7) into protekliTjedni;
if new.datum_zaceca<>old.datum_zaceca THEN
Update "Tjedan trudnoce"
set "Broj tjedna"=protekliTjedni
where idtjedantrudnoce=old.idtjedantrudnoce;
end if;
return new;
END;$$;
 9   DROP FUNCTION public.trigger_azurirajbrojtjednaupdate();
       public          postgres    false            ?            1259    16487    id_seq_idkorracun    SEQUENCE     z   CREATE SEQUENCE public.id_seq_idkorracun
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.id_seq_idkorracun;
       public          postgres    false            ?            1259    16488    Korisnicki Racun    TABLE     8  CREATE TABLE public."Korisnicki Racun" (
    "idKorisnicki racun" integer DEFAULT nextval('public.id_seq_idkorracun'::regclass) NOT NULL,
    "korisnicko ime" character varying(45) NOT NULL,
    lozinka character varying(45) NOT NULL,
    "datum kreiranja racuna" date DEFAULT CURRENT_DATE NOT NULL,
    "zadnja prijava" timestamp without time zone,
    ime character varying(45) NOT NULL,
    prezime character varying(45) NOT NULL,
    "e-mail" character varying(45) NOT NULL,
    "broj mobitela" character varying(45) NOT NULL,
    "datum rodenja" date NOT NULL
);
 &   DROP TABLE public."Korisnicki Racun";
       public         heap    postgres    false    209            ?            1259    16525    Razvoj bebe    TABLE     ?   CREATE TABLE public."Razvoj bebe" (
    "idRazvoj bebe" integer NOT NULL,
    "Mjesec trudnoce" integer NOT NULL,
    opis text
);
 !   DROP TABLE public."Razvoj bebe";
       public         heap    postgres    false            ?            1259    16571    Tjedan trudnoce    TABLE     ?   CREATE TABLE public."Tjedan trudnoce" (
    idtjedantrudnoce integer NOT NULL,
    "Broj tjedna" integer,
    korisnickiracunid integer NOT NULL,
    datum_zaceca date
);
 %   DROP TABLE public."Tjedan trudnoce";
       public         heap    postgres    false            ?            1259    16570 $   Tjedan trudnoce_idtjedantrudnoce_seq    SEQUENCE     ?   CREATE SEQUENCE public."Tjedan trudnoce_idtjedantrudnoce_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public."Tjedan trudnoce_idtjedantrudnoce_seq";
       public          postgres    false    213            7           0    0 $   Tjedan trudnoce_idtjedantrudnoce_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public."Tjedan trudnoce_idtjedantrudnoce_seq" OWNED BY public."Tjedan trudnoce".idtjedantrudnoce;
          public          postgres    false    212            ?            1259    16618    biljeska_idBiljeska_seq    SEQUENCE     ?   CREATE SEQUENCE public."biljeska_idBiljeska_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public."biljeska_idBiljeska_seq";
       public          postgres    false            ?            1259    16619    biljeska    TABLE       CREATE TABLE public.biljeska (
    "idBiljeska" integer DEFAULT nextval('public."biljeska_idBiljeska_seq"'::regclass) NOT NULL,
    mjesec integer NOT NULL,
    "KorisnickiRacunID" integer NOT NULL,
    zadnji_update timestamp without time zone,
    biljeska text
);
    DROP TABLE public.biljeska;
       public         heap    postgres    false    214            ?            1259    16766    biljeska - sortiranje     VIEW     <  CREATE VIEW public."biljeska - sortiranje " AS
 SELECT p.ime,
    p.prezime,
    biljeska.zadnji_update AS "vrijeme zadnjeg
žauriranja",
    biljeska.biljeska
   FROM public.biljeska,
    public."Korisnicki Racun" p
  WHERE (p."idKorisnicki racun" = biljeska."KorisnickiRacunID")
  ORDER BY biljeska.zadnji_update;
 +   DROP VIEW public."biljeska - sortiranje ";
       public          postgres    false    210    215    215    215    210    210            ?            1259    16739 	   login_log    TABLE     ?   CREATE TABLE public.login_log (
    idlog integer NOT NULL,
    korisnickiracunid integer NOT NULL,
    datum_logina timestamp without time zone NOT NULL
);
    DROP TABLE public.login_log;
       public         heap    postgres    false            ?            1259    16738    login_log_idlog_seq    SEQUENCE     ?   CREATE SEQUENCE public.login_log_idlog_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.login_log_idlog_seq;
       public          postgres    false    217            8           0    0    login_log_idlog_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.login_log_idlog_seq OWNED BY public.login_log.idlog;
          public          postgres    false    216            ?            1259    16762    pregled tjedna trudnoce    VIEW     ?   CREATE VIEW public."pregled tjedna trudnoce" AS
 SELECT p.ime AS "Ime",
    p.prezime AS "Prezime",
    t."Broj tjedna"
   FROM public."Korisnicki Racun" p,
    public."Tjedan trudnoce" t
  WHERE (p."idKorisnicki racun" = t.korisnickiracunid);
 ,   DROP VIEW public."pregled tjedna trudnoce";
       public          postgres    false    210    210    210    213    213            ?           2604    16574     Tjedan trudnoce idtjedantrudnoce    DEFAULT     ?   ALTER TABLE ONLY public."Tjedan trudnoce" ALTER COLUMN idtjedantrudnoce SET DEFAULT nextval('public."Tjedan trudnoce_idtjedantrudnoce_seq"'::regclass);
 Q   ALTER TABLE public."Tjedan trudnoce" ALTER COLUMN idtjedantrudnoce DROP DEFAULT;
       public          postgres    false    213    212    213            ?           2604    16742    login_log idlog    DEFAULT     r   ALTER TABLE ONLY public.login_log ALTER COLUMN idlog SET DEFAULT nextval('public.login_log_idlog_seq'::regclass);
 >   ALTER TABLE public.login_log ALTER COLUMN idlog DROP DEFAULT;
       public          postgres    false    216    217    217            )          0    16488    Korisnicki Racun 
   TABLE DATA           ?   COPY public."Korisnicki Racun" ("idKorisnicki racun", "korisnicko ime", lozinka, "datum kreiranja racuna", "zadnja prijava", ime, prezime, "e-mail", "broj mobitela", "datum rodenja") FROM stdin;
    public          postgres    false    210   ?Q       *          0    16525    Razvoj bebe 
   TABLE DATA           Q   COPY public."Razvoj bebe" ("idRazvoj bebe", "Mjesec trudnoce", opis) FROM stdin;
    public          postgres    false    211   ?R       ,          0    16571    Tjedan trudnoce 
   TABLE DATA           m   COPY public."Tjedan trudnoce" (idtjedantrudnoce, "Broj tjedna", korisnickiracunid, datum_zaceca) FROM stdin;
    public          postgres    false    213   qV       .          0    16619    biljeska 
   TABLE DATA           f   COPY public.biljeska ("idBiljeska", mjesec, "KorisnickiRacunID", zadnji_update, biljeska) FROM stdin;
    public          postgres    false    215   ?V       0          0    16739 	   login_log 
   TABLE DATA           K   COPY public.login_log (idlog, korisnickiracunid, datum_logina) FROM stdin;
    public          postgres    false    217   ?W       9           0    0 $   Tjedan trudnoce_idtjedantrudnoce_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public."Tjedan trudnoce_idtjedantrudnoce_seq"', 3, true);
          public          postgres    false    212            :           0    0    biljeska_idBiljeska_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public."biljeska_idBiljeska_seq"', 50, true);
          public          postgres    false    214            ;           0    0    id_seq_idkorracun    SEQUENCE SET     @   SELECT pg_catalog.setval('public.id_seq_idkorracun', 12, true);
          public          postgres    false    209            <           0    0    login_log_idlog_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.login_log_idlog_seq', 7, true);
          public          postgres    false    216            ?           2606    16494 &   Korisnicki Racun Korisnicki Racun_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public."Korisnicki Racun"
    ADD CONSTRAINT "Korisnicki Racun_pkey" PRIMARY KEY ("idKorisnicki racun");
 T   ALTER TABLE ONLY public."Korisnicki Racun" DROP CONSTRAINT "Korisnicki Racun_pkey";
       public            postgres    false    210            ?           2606    16631    Razvoj bebe Razvoj bebe_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public."Razvoj bebe"
    ADD CONSTRAINT "Razvoj bebe_pkey" PRIMARY KEY ("idRazvoj bebe");
 J   ALTER TABLE ONLY public."Razvoj bebe" DROP CONSTRAINT "Razvoj bebe_pkey";
       public            postgres    false    211            ?           2606    16757 "   Tjedan trudnoce UniqueIDConstraint 
   CONSTRAINT     n   ALTER TABLE ONLY public."Tjedan trudnoce"
    ADD CONSTRAINT "UniqueIDConstraint" UNIQUE (korisnickiracunid);
 P   ALTER TABLE ONLY public."Tjedan trudnoce" DROP CONSTRAINT "UniqueIDConstraint";
       public            postgres    false    213            ?           2606    16624    biljeska biljeska_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.biljeska
    ADD CONSTRAINT biljeska_pkey PRIMARY KEY ("idBiljeska");
 @   ALTER TABLE ONLY public.biljeska DROP CONSTRAINT biljeska_pkey;
       public            postgres    false    215            ?           2606    16744    login_log pkeyLog 
   CONSTRAINT     T   ALTER TABLE ONLY public.login_log
    ADD CONSTRAINT "pkeyLog" PRIMARY KEY (idlog);
 =   ALTER TABLE ONLY public.login_log DROP CONSTRAINT "pkeyLog";
       public            postgres    false    217            ?           2606    16761    Tjedan trudnoce pkeyTrudnoca 
   CONSTRAINT     l   ALTER TABLE ONLY public."Tjedan trudnoce"
    ADD CONSTRAINT "pkeyTrudnoca" PRIMARY KEY (idtjedantrudnoce);
 J   ALTER TABLE ONLY public."Tjedan trudnoce" DROP CONSTRAINT "pkeyTrudnoca";
       public            postgres    false    213            ?           2620    16592    Tjedan trudnoce azuriraj_tjedan    TRIGGER     ?   CREATE TRIGGER azuriraj_tjedan AFTER INSERT ON public."Tjedan trudnoce" FOR EACH ROW EXECUTE FUNCTION public.trigger_azurirajbrojtjedna();
 :   DROP TRIGGER azuriraj_tjedan ON public."Tjedan trudnoce";
       public          postgres    false    238    213            ?           2620    16596 %   Tjedan trudnoce azuriraj_tjedanupdate    TRIGGER     ?   CREATE TRIGGER azuriraj_tjedanupdate AFTER UPDATE ON public."Tjedan trudnoce" FOR EACH ROW EXECUTE FUNCTION public.trigger_azurirajbrojtjednaupdate();
 @   DROP TRIGGER azuriraj_tjedanupdate ON public."Tjedan trudnoce";
       public          postgres    false    213    221            ?           2620    16643    Korisnicki Racun dodajbiljeske    TRIGGER     ?   CREATE TRIGGER dodajbiljeske AFTER INSERT ON public."Korisnicki Racun" FOR EACH ROW EXECUTE FUNCTION public.dodajpraznebiljeske();
 9   DROP TRIGGER dodajbiljeske ON public."Korisnicki Racun";
       public          postgres    false    210    237            ?           2620    16737    biljeska provjeriMjesec    TRIGGER     ?   CREATE TRIGGER "provjeriMjesec" BEFORE UPDATE OF biljeska ON public.biljeska FOR EACH ROW EXECUTE FUNCTION public.provjerimjesec();
 2   DROP TRIGGER "provjeriMjesec" ON public.biljeska;
       public          postgres    false    240    215    215            ?           2620    16751    Korisnicki Racun updateLog    TRIGGER     ?   CREATE TRIGGER "updateLog" BEFORE UPDATE OF "zadnja prijava" ON public."Korisnicki Racun" FOR EACH ROW EXECUTE FUNCTION public.dodajlog();
 7   DROP TRIGGER "updateLog" ON public."Korisnicki Racun";
       public          postgres    false    210    241    210            ?           2606    16745    login_log fkKorisnica    FK CONSTRAINT     ?   ALTER TABLE ONLY public.login_log
    ADD CONSTRAINT "fkKorisnica" FOREIGN KEY (korisnickiracunid) REFERENCES public."Korisnicki Racun"("idKorisnicki racun");
 A   ALTER TABLE ONLY public.login_log DROP CONSTRAINT "fkKorisnica";
       public          postgres    false    210    217    3208            ?           2606    16625    biljeska fk_biljeska    FK CONSTRAINT     ?   ALTER TABLE ONLY public.biljeska
    ADD CONSTRAINT fk_biljeska FOREIGN KEY ("KorisnickiRacunID") REFERENCES public."Korisnicki Racun"("idKorisnicki racun");
 >   ALTER TABLE ONLY public.biljeska DROP CONSTRAINT fk_biljeska;
       public          postgres    false    3208    215    210            ?           2606    16577    Tjedan trudnoce fk_ttrudnoce    FK CONSTRAINT     ?   ALTER TABLE ONLY public."Tjedan trudnoce"
    ADD CONSTRAINT fk_ttrudnoce FOREIGN KEY (korisnickiracunid) REFERENCES public."Korisnicki Racun"("idKorisnicki racun");
 H   ALTER TABLE ONLY public."Tjedan trudnoce" DROP CONSTRAINT fk_ttrudnoce;
       public          postgres    false    210    3208    213            )     x?u?Mn? F??)r[̀????6??.?Ʊ?T??#?b=XWu?4????4|???)? HBv@???ؠ?ns??^򞋖?F?*T??|???R{?߀
B@kU?r1???ڕ6??t?l??%??-??RU?#2??Đãw{??u[?C?w?'?
??4??????˭???}j/???2Ɣ?m??!????ō???1?>????????"??X??Ԕ<92??у?U'KP[?Ez?I#???!???Q?(qd?Jhvjc_L?n?      *   ?  x??U;??6??S??X?K?pS???)i?(	?@?/?????E&ؒ??נ?{9??(???^?n??U???jE?k\????k?KE=WL8h\t??*ڬ?l5N?????]j?h???e?9?Anp-y+W4u???գN5?@)R??z??I?GI???)?4??VS?1???&??HG?#ʝ?G?`????O䌣e??P?R%?WK?|?5??l?wE?|?????Ov?̖I???b????U??Q9???H????·+?@?? =p???\?b??*[W߳Jh?R?????G?/???](-7?
?? ???k-?P=?"6????GTJ4?B?*?(???????b?IJ)?7IW????|}Q????l3?߅?k@??s?,?;?? ?^^>	7@Ł??]_&E? l?Z?M??/????swȇKx@U?]??????f*??$?`?\?]?+]_?M?|??sO???b?m?j?D???7??۠??㬙?=Z?.??u~p??޵0??|?A!İS ??>+5???	?P???W(e?V?ɻ???֜??=?c???????????l???g????F9?>?X??:??$?ҝB<I?x??5??gD? L??N??-	??Iߣ^mfA????}??A?ز?_?5??iC???AL??G5?3y?8h?Z@;?Y%W?|;o???!;̡?F?4?c2?De???m]?ؤa`?.^!?r?dj?G?G??b?{?n?>???þƮ?(g????څ?`/+/???s#??e?{:?X???Z??Q?G?? ?δ?]?F@??ߧ3Q?}??A??vv????lez?0????f?????S??q???n??~)??????v?+??(??>?I6<?զ?Am?ƳC?R??iw^??v???wL?U%R??r??#??^/?Y???T7???9?|?X?t??       ,   '   x?3?4?44?4202?54?56?2?a"@d????? ??M      .   2  x?e?]n?0??Sp?"{mc?c??B?(?T???ww+N[?Ďd?0???r??K?0gʘ?M?=???????????xy_???m?????u?:?????e 7?$??"?46(?	?ĳ?'j??6?B#uh??Ԣ?j4R?F*?HM@AU@?lsĎ????{?g??T??xΉ?M?9rV???9?C̙c??Z?/????}?_ˏ?{?;?˩0??^??ӯ#???` ?` ?` ?` V)Z0??p%s??\@?2????d.???T
򁻤??y?qn`iZ?޺j?e???
??      0   [   x?m??	?0?w5E??e;?3K???????^:????t?O?????&9S?҆??MFe?#7?Z?ҭ? ???FV&?Ʊ>?pt??[ <? ?     